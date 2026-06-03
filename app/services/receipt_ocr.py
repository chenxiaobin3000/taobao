import threading
import os
import re
import tempfile


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
            return cls.recognize(temp_path)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

    @staticmethod
    def get_text(lines):
        return '\n'.join([line['text'] for line in lines if line.get('text')])

    @classmethod
    def parse_common(cls, text, receipt_items):
        project = cls._match_project(text, receipt_items)
        if not project:
            raise ValueError('未识别到发票项目')
        return {
            'create_date': cls._parse_date(text),
            'project_id': project['id'],
            'project_num': cls._parse_num(text),
            'receipt_note': 'OCR识别'
        }

    @classmethod
    def parse_to(cls, text, receipt_items):
        data = cls.parse_common(text, receipt_items)
        data['receipt_id'] = cls._parse_tax_id(text)
        data['receipt_name'] = cls._parse_receipt_name(text)
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
        name = re.split(r'(纳税人识别号|统一社会信用代码|税号|地址|电话|开户行|账号)', match.group(1))[0].strip()
        if not name:
            raise ValueError('未识别到抬头')
        return name[:20]

    @staticmethod
    def _match_project(text, receipt_items):
        for item in receipt_items:
            project_name = item.get('project_name')
            if project_name and project_name in text:
                return item
        return None

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
