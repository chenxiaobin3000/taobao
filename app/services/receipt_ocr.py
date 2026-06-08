import threading
import os
import re
import tempfile
from decimal import Decimal


class ReceiptOCR:
    _lock = threading.Lock()
    _ocr = None

    @classmethod
    def recognize(cls, image_path):
        ocr = cls._get_ocr()
        if hasattr(ocr, 'predict'):
            return cls._normalize_predict_result(ocr.predict(input=image_path))
        return cls._normalize_ocr_result(ocr.ocr(image_path, cls=True))

    @classmethod
    def recognize_upload(cls, upload_file):
        suffix = os.path.splitext(upload_file.name)[1] or '.pdf'
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_path = temp_file.name
                for chunk in upload_file.chunks():
                    temp_file.write(chunk)
            if suffix.lower() == '.pdf':
                text = cls._extract_pdf_text(temp_path)
                if cls._is_valid_pdf_text(text):
                    return cls._text_to_lines(text)
            return cls.recognize(temp_path)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

    @staticmethod
    def get_text(lines):
        return '\n'.join([line['text'] for line in lines if line.get('text')])

    @staticmethod
    def _extract_pdf_text(pdf_path):
        try:
            from pypdf import PdfReader
        except ImportError:
            return ''
        try:
            reader = PdfReader(pdf_path)
            texts = []
            for page in reader.pages:
                page_text = page.extract_text() or ''
                if page_text:
                    texts.append(page_text)
            return '\n'.join(texts)
        except Exception:
            return ''

    @staticmethod
    def _is_valid_pdf_text(text):
        if not text:
            return False
        compact_text = re.sub(r'\s+', '', text)
        return '发票' in compact_text and ('项目名称' in compact_text or '开票日期' in compact_text)

    @staticmethod
    def _text_to_lines(text):
        return [{'text': line.strip(), 'score': None, 'box': None} for line in text.splitlines() if line.strip()]

    @classmethod
    def parse_common(cls, text, receipt_items, create_project=None):
        project = cls._match_project(text, receipt_items)
        if not project:
            project_name = cls._parse_project_name(text)
            if project_name and create_project:
                project = create_project(project_name)
            if not project:
                preview = cls._compact_text(text)[:500]
                if preview:
                    projects = cls._format_projects(receipt_items)
                    if projects:
                        raise ValueError(f'未识别到发票项目，识别内容：{preview}；已配置项目：{projects}')
                    raise ValueError(f'未识别到发票项目，识别内容：{preview}')
                raise ValueError('未识别到发票项目')
        return {
            'create_date': cls._parse_date(text),
            'project_id': project['id'],
            'project_num': cls._parse_num(text),
            'amount': cls._parse_amount(text),
            'tax': cls._parse_tax(text),
            'tax_rate': cls._parse_tax_rate(text),
            'company': cls._parse_seller_name(text),
            'company_id': cls._parse_seller_id(text),
            'receipt_note': '文件扫描'
        }

    @classmethod
    def parse_to(cls, text, receipt_items, create_project=None):
        data = cls.parse_common(text, receipt_items, create_project)
        data['company'] = cls._parse_receipt_name(text)
        data['company_id'] = cls._parse_company_id(text)
        return data

    @classmethod
    def _get_ocr(cls):
        if cls._ocr is None:
            with cls._lock:
                if cls._ocr is None:
                    try:
                        from paddleocr import PaddleOCR
                    except ImportError as exc:
                        raise RuntimeError('PaddleOCR未安装，请先安装requirements.txt中的paddlepaddle和paddleocr') from exc
                    cls._ocr = cls._create_ocr(PaddleOCR)
        return cls._ocr

    @staticmethod
    def _parse_date(text):
        patterns = [
            r'开票日期[:：]?\s*(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'日期[:：]?\s*(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                year, month, day = match.groups()
                return f'{int(year):04d}-{int(month):02d}-{int(day):02d}'
        raise ValueError('未识别到开票日期')

    @staticmethod
    def _parse_num(text):
        match = re.search(r'数量[:：]?\s*(\d+)', text)
        if match:
            return int(match.group(1))
        return 1

    @staticmethod
    def _parse_project_name(text):
        match = re.search(r'\*[^*\s]{1,20}\*[^ \t\r\n]{1,30}', text)
        if not match:
            return ''
        return match.group(0).strip(' ，,;；')[:20]

    @staticmethod
    def _parse_amount(text):
        match = re.search(r'合\s*计\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)', text)
        if match:
            return Decimal(match.group(1)).quantize(Decimal('0.01'))
        amounts = re.findall(r'[￥¥]\s*([0-9]+(?:\.[0-9]+)?)', text)
        if amounts:
            return Decimal(amounts[0]).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @staticmethod
    def _parse_tax(text):
        match = re.search(r'合\s*计\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)', text)
        if match:
            return Decimal(match.group(2)).quantize(Decimal('0.01'))
        amounts = re.findall(r'[￥¥]\s*([0-9]+(?:\.[0-9]+)?)', text)
        if len(amounts) > 1:
            return Decimal(amounts[1]).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @staticmethod
    def _parse_tax_rate(text):
        match = re.search(r'(\d+)\s*%', text)
        if not match:
            return 0
        return int(match.group(1))

    @staticmethod
    def _parse_company_id(text):
        match = re.search(r'购买方信息[\s\S]{0,120}?(?:纳税人识别号|统一社会信用代码|税号)[:：]\s*([0-9A-Z]{15,20})', text)
        if not match:
            match = re.search(r'(?:纳税人识别号|统一社会信用代码|税号)[:：]\s*([0-9A-Z]{15,20})', text)
        if not match:
            return ''
        return match.group(1)[:20]

    @staticmethod
    def _parse_seller_id(text):
        seller_text = text
        seller_index = text.find('销售方信息')
        if seller_index >= 0:
            seller_text = text[seller_index:]
        seller_tax_ids = re.findall(r'(?:纳税人识别号|统一社会信用代码|税号)[:：]\s*([0-9A-Z]{15,20})', seller_text)
        if seller_tax_ids:
            return seller_tax_ids[-1][:20]
        tax_ids = re.findall(r'(?:纳税人识别号|统一社会信用代码|税号)[:：]\s*([0-9A-Z]{15,20})', text)
        if tax_ids:
            return tax_ids[-1][:20]
        return ''

    @staticmethod
    def _parse_tax_id(text):
        match = re.search(r'(?:纳税人识别号|统一社会信用代码|税号)[:：]?\s*([0-9A-Z]{15,20})', text)
        if not match:
            match = re.search(r'\b([0-9A-Z]{15,20})\b', text)
        if not match:
            raise ValueError('未识别到税号')
        tax_id = re.sub(r'\D', '', match.group(1))
        if not tax_id:
            raise ValueError('税号不是数字，当前字段无法保存')
        return tax_id[:18]

    @staticmethod
    def _parse_receipt_name(text):
        match = re.search(r'购买方信息[\s\S]{0,80}?名称[:：]\s*([^\n]+)', text)
        if not match:
            match = re.search(r'名称[:：]\s*([^\n]+)', text)
        if not match:
            raise ValueError('未识别到抬头')
        name = re.split(r'(销售方信息|纳税人识别号|统一社会信用代码|税号|地址|电话|开户行|账号)', match.group(1))[0].strip()
        if not name:
            raise ValueError('未识别到抬头')
        return name[:20]

    @staticmethod
    def _parse_seller_name(text):
        match = re.search(r'销售方信息[\s\S]{0,120}?名称[:：]\s*([^\n]+)', text)
        if not match:
            return ''
        name = re.split(r'(购买方信息|纳税人识别号|统一社会信用代码|税号|地址|电话|开户行|账号)', match.group(1))[0].strip()
        if not name:
            return ''
        return name[:20]

    @staticmethod
    def _match_project(text, receipt_items):
        norm_text = ReceiptOCR._normalize_match_text(text)
        for item in receipt_items:
            project_name = item.get('project_name')
            project_note = item.get('project_note')
            for keyword in ReceiptOCR._iter_keywords(project_name):
                if ReceiptOCR._match_keyword(norm_text, keyword):
                    return item
            for keyword in ReceiptOCR._iter_keywords(project_note):
                if ReceiptOCR._match_keyword(norm_text, keyword):
                    return item
        return None

    @staticmethod
    def _iter_keywords(value):
        if not value:
            return []
        return [keyword for keyword in re.split(r'[,，、;；|/\s]+', str(value)) if keyword]

    @staticmethod
    def _match_keyword(norm_text, keyword):
        norm_keyword = ReceiptOCR._normalize_match_text(keyword)
        return bool(norm_keyword and norm_keyword in norm_text)

    @staticmethod
    def _normalize_match_text(value):
        if not value:
            return ''
        value = str(value).lower()
        return re.sub(r'[\s\W_]+', '', value)

    @staticmethod
    def _compact_text(value):
        if not value:
            return ''
        return re.sub(r'\s+', ' ', str(value)).strip()

    @staticmethod
    def _format_projects(receipt_items):
        values = []
        for item in receipt_items[:20]:
            name = item.get('project_name')
            note = item.get('project_note')
            if name and note:
                values.append(f'{name}({note})')
            elif name:
                values.append(str(name))
        return '，'.join(values)

    @staticmethod
    def _create_ocr(paddle_ocr):
        try:
            return paddle_ocr(use_textline_orientation=True, lang='ch')
        except TypeError:
            return paddle_ocr(use_angle_cls=True, lang='ch')

    @classmethod
    def _normalize_predict_result(cls, result):
        lines = []
        if not result:
            return lines
        for page in result:
            if hasattr(page, 'json'):
                page = page.json
            if isinstance(page, dict):
                page = page.get('res', page)
                texts = page.get('rec_texts') or []
                scores = page.get('rec_scores') or []
                boxes = page.get('rec_polys') or page.get('dt_polys') or []
                for index, text in enumerate(texts):
                    lines.append({
                        'text': text,
                        'score': cls._get_item(scores, index),
                        'box': cls._to_list(cls._get_item(boxes, index))
                    })
        return lines

    @classmethod
    def _normalize_ocr_result(cls, result):
        lines = []
        if not result:
            return lines
        pages = result if isinstance(result, list) else [result]
        for page in pages:
            if not page:
                continue
            for item in page:
                if not item or len(item) < 2:
                    continue
                text_info = item[1]
                text = text_info[0] if text_info else ''
                score = text_info[1] if text_info and len(text_info) > 1 else None
                lines.append({
                    'text': text,
                    'score': score,
                    'box': cls._to_list(item[0])
                })
        return lines

    @staticmethod
    def _get_item(items, index):
        if index >= len(items):
            return None
        return items[index]

    @staticmethod
    def _to_list(value):
        if value is None:
            return None
        if hasattr(value, 'tolist'):
            return value.tolist()
        if isinstance(value, tuple):
            return list(value)
        return value
