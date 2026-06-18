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
            'receipt_id': cls._parse_receipt_id(text),
            'create_date': cls._parse_date(text),
            'project_id': project['id'],
            'project_num': cls._parse_num(text, project.get('project_name')),
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
    def _parse_receipt_id(text):
        patterns = [
            r'发票\s*号码\s*[:：]?\s*([0-9]{8,20})',
            r'发票\s*号\s*码\s*[:：]?\s*([0-9]{8,20})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)[:20]

        compact_text = re.sub(r'\s+', '', text)
        compact_patterns = [
            r'发票号码[:：]?([0-9]{8,20})',
            r'发票代码[:：]?[0-9]{8,12}发票号码[:：]?([0-9]{8,20})',
        ]
        for pattern in compact_patterns:
            match = re.search(pattern, compact_text)
            if match:
                return match.group(1)[:20]

        numbers = re.findall(r'\b([0-9]{20})\b', text)
        if numbers:
            return numbers[0][:20]
        spaced_numbers = re.findall(r'(?<![0-9])((?:[0-9]\s*){20})(?![0-9])', text)
        if spaced_numbers:
            return re.sub(r'\s+', '', spaced_numbers[0])[:20]
        raise ValueError('未识别到发票号码')

    @staticmethod
    def _parse_date(text):
        text = ReceiptOCR._compact_number_spaces(text)
        patterns = [
            r'开票日期[:：]?\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
            r'日期[:：]?\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
            r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
            r'(?<!\d)(20\d{2})\D{1,4}(\d{1,2})\D{1,4}(\d{1,2})(?!\d)',
            r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                year, month, day = match.groups()
                return f'{int(year):04d}-{int(month):02d}-{int(day):02d}'
        raise ValueError('未识别到开票日期')

    @staticmethod
    def _parse_num(text, project_name=None):
        match = re.search(r'数量[:：]?\s*(\d+)', text)
        if match:
            return int(match.group(1))
        if project_name:
            count = ReceiptOCR._count_project_rows(text, project_name)
            if count > 1:
                return count
            amount_count = ReceiptOCR._parse_num_by_amount(text, project_name)
            if amount_count > 1:
                return amount_count
        return 1

    @staticmethod
    def _count_project_rows(text, project_name):
        norm_project = ReceiptOCR._normalize_match_text(project_name)
        if not norm_project:
            return 1
        count = 0
        for line in re.split(r'[\r\n]+', text):
            if ReceiptOCR._match_keyword(ReceiptOCR._normalize_match_text(line), project_name):
                count += 1
        if count > 1:
            return count

        norm_text = ReceiptOCR._normalize_match_text(text)
        count = norm_text.count(norm_project)
        return count if count > 0 else 1

    @staticmethod
    def _parse_num_by_amount(text, project_name):
        amount = ReceiptOCR._parse_amount(text)
        tax = ReceiptOCR._parse_tax(text)
        if amount <= 0:
            return 1
        for line in re.split(r'[\r\n]+', text):
            if not ReceiptOCR._match_keyword(ReceiptOCR._normalize_match_text(line), project_name):
                continue
            unit_price = ReceiptOCR._parse_unit_price_from_line(line, amount, tax)
            if unit_price <= 0:
                continue
            count = amount / unit_price
            rounded_count = int(count.to_integral_value())
            if rounded_count > 1 and abs(count - rounded_count) <= Decimal('0.02'):
                return rounded_count
        return 1

    @staticmethod
    def _parse_unit_price_from_line(line, amount, tax):
        compact_line = re.sub(r'\s+', '', line)
        tax_text = format(tax, 'f').rstrip('0').rstrip('.')
        if tax_text:
            tax_index = compact_line.find(tax_text)
            if tax_index >= 0:
                tail = compact_line[tax_index + len(tax_text):]
                tail_number = re.search(r'([0-9]+(?:\.[0-9]+)?)', tail)
                if tail_number:
                    return Decimal(tail_number.group(1))

        numbers = [Decimal(value) for value in re.findall(r'[0-9]+(?:\.[0-9]+)?', line)]
        candidates = [value for value in numbers if value > 0 and value < amount and value != tax]
        if candidates:
            return candidates[-1]
        return Decimal('0.00')

    @staticmethod
    def _parse_project_name(text):
        star_project_name = ReceiptOCR._parse_star_project_name(text)
        if star_project_name:
            return star_project_name
        patterns = [
            r'项目名称[\s\S]{0,80}?([^\s￥¥\d]{1,20}\*[^ \t\r\n￥¥]{1,30})',
            r'\*[^*\s]{1,20}\*[^ \t\r\n￥¥]{1,30}',
            r'[\u4e00-\u9fa5]{1,20}\*[\u4e00-\u9fa5A-Za-z0-9（）()\-]{1,30}'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1) if match.lastindex else match.group(0)
                value = re.split(r'(规格型号|单位|数量|单价|金额|税率|税额|合\s*计)', value)[0]
                return value.strip(' ，,;；')[:20]
        for token in re.split(r'\s+', text):
            if '*' in token and not token.startswith('*'):
                value = re.split(r'[￥¥\d]', token)[0]
                if value:
                    return value.strip(' ，,;；')[:20]
        return ''

    @staticmethod
    def _parse_amount(text):
        text = ReceiptOCR._compact_number_spaces(text)
        match = re.search(r'合\s*计\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)', text)
        if match:
            return Decimal(match.group(1)).quantize(Decimal('0.01'))
        amounts = re.findall(r'[￥¥]\s*([0-9]+(?:\.[0-9]+)?)', text)
        if amounts:
            return Decimal(amounts[0]).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @staticmethod
    def _parse_tax(text):
        text = ReceiptOCR._compact_number_spaces(text)
        match = re.search(r'合\s*计\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)\s*[￥¥]?\s*([0-9]+(?:\.[0-9]+)?)', text)
        if match:
            return Decimal(match.group(2)).quantize(Decimal('0.01'))
        amounts = re.findall(r'[￥¥]\s*([0-9]+(?:\.[0-9]+)?)', text)
        if len(amounts) > 1:
            return Decimal(amounts[1]).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @staticmethod
    def _parse_tax_rate(text):
        text = ReceiptOCR._compact_number_spaces(text)
        match = re.search(r'(\d+)\s*%', text)
        if not match:
            return 0
        return int(match.group(1))

    @staticmethod
    def _parse_company_id(text):
        buyer_text = ReceiptOCR._parse_party_text(text, '购买方信息', '销售方信息')
        match = re.search(r'(?:纳税人识别号|统一社会信用代码|税号)[:：]\s*([0-9A-Z]{15,20})', buyer_text)
        if match:
            return match.group(1)[:20]
        buyer_name = ReceiptOCR._parse_receipt_name(text)
        if '个人' in buyer_name:
            return ''
        tax_ids = re.findall(r'(?:纳税人识别号|统一社会信用代码|税号)[:：]\s*([0-9A-Z]{15,20})', text)
        if len(tax_ids) >= 2:
            return tax_ids[0][:20]
        if len(tax_ids) == 1 and tax_ids[0] != ReceiptOCR._parse_seller_id(text):
            return tax_ids[0][:20]
        spaced_tax_ids = ReceiptOCR._parse_spaced_tax_ids(text)
        if spaced_tax_ids:
            return spaced_tax_ids[0][:20]
        return ''

    @staticmethod
    def _parse_star_project_name(text):
        match = re.search(
            r'\*\s*((?:[\u4e00-\u9fa5A-Za-z]\s*){1,20})'
            r'\*\s*((?:[\u4e00-\u9fa5A-Za-z]\s*){1,30}?)'
            r'(?=\s+\d\s*%|\s+\d+(?:\s*\.\s*\d+)?|[\r\n]|$)',
            text
        )
        if not match:
            return ''
        category = re.sub(r'\s+', '', match.group(1))
        name = re.sub(r'\s+', '', match.group(2))
        if not category or not name:
            return ''
        return f'*{category}*{name}'[:20]

    @staticmethod
    def _parse_party_text(text, start_keyword, end_keyword):
        start_index = text.find(start_keyword)
        if start_index < 0:
            return ''
        end_index = text.find(end_keyword, start_index + len(start_keyword))
        if end_index < 0:
            return text[start_index:]
        return text[start_index:end_index]

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
        spaced_tax_ids = ReceiptOCR._parse_spaced_tax_ids(text)
        if spaced_tax_ids:
            if len(spaced_tax_ids) >= 2:
                return spaced_tax_ids[1][:20]
            return spaced_tax_ids[0][:20]
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
        if match:
            name = re.split(r'(销售方信息|纳税人识别号|统一社会信用代码|税号|地址|电话|开户行|账号)', match.group(1))[0].strip()
            name = ReceiptOCR._clean_party_name(name)
            if name:
                return name[:20]
        names = ReceiptOCR._parse_pdf_party_names(text)
        if names:
            return names[0][:20]
        raise ValueError('未识别到抬头')

    @staticmethod
    def _parse_seller_name(text):
        match = re.search(r'销售方信息[\s\S]{0,120}?名称[:：]\s*([^\n]+)', text)
        if match:
            name = re.split(r'(购买方信息|纳税人识别号|统一社会信用代码|税号|地址|电话|开户行|账号)', match.group(1))[0].strip()
            name = ReceiptOCR._clean_party_name(name)
            if name:
                return name[:20]
        names = ReceiptOCR._parse_pdf_party_names(text)
        if len(names) >= 2:
            return names[1][:20]
        return ''

    @staticmethod
    def _parse_spaced_tax_ids(text):
        text = ReceiptOCR._compact_number_spaces(text)
        values = []
        for match in re.finditer(r'(?<![0-9A-Z])((?:[0-9A-Z]\s*){15,20})', text):
            value = re.sub(r'\s+', '', match.group(1))
            if ReceiptOCR._is_tax_id_like(value) and not ReceiptOCR._is_bank_account_match(text, match):
                values.append(value)
        return values

    @staticmethod
    def _parse_pdf_party_names(text):
        text = ReceiptOCR._compact_number_spaces(text)
        tax_matches = []
        for match in re.finditer(r'(?<![0-9A-Z])((?:[0-9A-Z]\s*){15,20})', text):
            value = re.sub(r'\s+', '', match.group(1))
            if ReceiptOCR._is_tax_id_like(value) and not ReceiptOCR._is_bank_account_match(text, match):
                tax_matches.append(match)
        if len(tax_matches) == 1:
            return ReceiptOCR._parse_single_tax_party_names(text[:tax_matches[0].start()])
        if len(tax_matches) < 2:
            return []
        buyer_segment = text[:tax_matches[0].start()]
        seller_segment = text[tax_matches[0].end():tax_matches[1].start()]
        names = []
        for segment in [buyer_segment, seller_segment]:
            name = ReceiptOCR._extract_company_name(segment)
            if name:
                names.append(name)
        return names

    @staticmethod
    def _parse_single_tax_party_names(text):
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'\d{4}年\d{1,2}月\d{1,2}日', '', text)
        buyer_matches = list(re.finditer(r'[\u4e00-\u9fa5]{2,10}[（(]个人[）)]', text))
        if buyer_matches:
            buyer_match = buyer_matches[-1]
            buyer_name = ReceiptOCR._clean_party_name(buyer_match.group(0))
            seller_name = ReceiptOCR._extract_company_name(text[buyer_match.end():])
            names = []
            if buyer_name:
                names.append(buyer_name)
            if seller_name:
                names.append(seller_name)
            return names

        company_matches = list(re.finditer(r'[\u4e00-\u9fa5（）()]{2,40}?(?:有限公司|公司)', text))
        if not company_matches:
            return []

        seller_match = company_matches[-1]
        seller_name = ReceiptOCR._clean_party_name(seller_match.group(0))
        buyer_segment = text[:seller_match.start()]
        buyer_name = ''
        if len(company_matches) > 1:
            buyer_name = ReceiptOCR._clean_party_name(company_matches[-2].group(0))

        names = []
        if buyer_name:
            names.append(buyer_name)
        if seller_name:
            names.append(seller_name)
        return names

    @staticmethod
    def _is_tax_id_like(value):
        if not value:
            return False
        if re.search(r'[A-Z]', value) and re.search(r'\d', value) and 15 <= len(value) <= 20:
            return True
        return value.isdigit() and len(value) in [15, 18]

    @staticmethod
    def _is_bank_account_match(text, match):
        prefix = re.sub(r'\s+', '', text[max(0, match.start() - 20):match.start()])
        return bool(re.search(r'(银行账号|银行帐号|账号|帐号)[:：;；]?$', prefix))

    @staticmethod
    def _extract_company_name(text):
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'\d{4}年\d{1,2}月\d{1,2}日', '', text)
        matches = re.findall(r'[\u4e00-\u9fa5（）()]{2,40}?(?:有限公司|公司|大学|学院|学校|中学|小学|销售部|经营部|商行|工作室|厂|店|个人[）)]?)', text)
        if not matches:
            return ''
        return ReceiptOCR._clean_party_name(matches[-1])

    @staticmethod
    def _clean_party_name(name):
        if not name:
            return ''
        name = re.sub(r'\s+', '', name)
        name = re.sub(r'^(名称[:：]?)+', '', name)
        name = re.sub(r'^.*(?:价税合计|项目名称|规格型号|单位|数量|单价|金额|税率|税额|合计|备注|开票人)', '', name)
        name = re.split(r'(项目名称|规格型号|单位|数量|单价|金额|税率|税额|合计|价税合计|备注|开票人)', name)[0]
        if len(name) < 2 or name in ['名称', '购买方信息', '销售方信息', '购', '买', '销', '售']:
            return ''
        return name[:20]

    @staticmethod
    def _match_project(text, receipt_items):
        norm_text = ReceiptOCR._normalize_match_text(text)
        project_name = ReceiptOCR._parse_star_project_name(text)
        norm_project_name = ReceiptOCR._normalize_match_text(project_name)
        if norm_project_name:
            for item in receipt_items:
                item_name = ReceiptOCR._normalize_match_text(item.get('project_name'))
                if item_name == norm_project_name:
                    return item

        candidates = []
        for item in receipt_items:
            project_name = item.get('project_name')
            project_note = item.get('project_note')
            for keyword in ReceiptOCR._iter_keywords(project_name):
                candidates.append((len(ReceiptOCR._normalize_match_text(keyword)), item, keyword))
            for keyword in ReceiptOCR._iter_keywords(project_note):
                candidates.append((len(ReceiptOCR._normalize_match_text(keyword)), item, keyword))
        for _, item, keyword in sorted(candidates, key=lambda value: value[0], reverse=True):
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
        if len(norm_keyword) < 2:
            return False
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
    def _compact_number_spaces(value):
        if not value:
            return ''
        value = str(value)
        previous = None
        while previous != value:
            previous = value
            value = re.sub(r'(?<=[0-9])\s+(?=[0-9])', '', value)
            value = re.sub(r'(?<=[0-9])\s+(?=\.)', '', value)
            value = re.sub(r'(?<=\.)\s+(?=[0-9])', '', value)
        return value

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
