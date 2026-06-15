import io
import zipfile
from xml.sax.saxutils import escape

from app.models.const.good_origin_type import GoodOriginType
from app.models.const.good_status import GoodStatus
from app.models.const.good_stock_type import GoodStockType
from app.models.const.good_type import GoodType
from app.models.system.good import Good
from app.models.system.good_alias import GoodAlias
from app.models.system.good_follow import GoodFollow
from app.models.system.permission import Permission
from app.models.system.shop import Shop
from app.models.system.user import User
from app.models.system.user_shop import UserShop


INIT_PLACEHOLDER_FILES = [
    {'name': '订单', 'permission': 3001},
    {'name': '推广', 'permission': 3003},
    {'name': '推广明细', 'permission': 3004},
    {'name': '扣费', 'permission': 3005},
    {'name': '聚合', 'permission': 3007},
    {'name': '退货', 'permission': 3009},
    {'name': '打款', 'permission': 3011},
    {'name': '采购', 'permission': 3012}
]
GOOD_EXPORT_HEADERS = ['名称', 'id', '优先级', '类型', '状态', '淘宝id', '外部', '进货id', '进货渠道', '完整名称', '别名1', '别名2', '别名3', '别名4', '别名5']


def build_init_zip(company_id, user_id):
    shops = get_user_shops(company_id, user_id)
    if not shops:
        raise ValueError('当前账号没有可用店铺')
    permissions = get_user_permissions(user_id)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as package:
        for shop in shops:
            folder = safe_zip_name(shop['name'])
            if 2003 in permissions:
                goods = build_good_export_rows(shop['id'])
                package.writestr(folder + '/商品.xlsx', build_xlsx(goods))
            for item in INIT_PLACEHOLDER_FILES:
                if item['permission'] in permissions:
                    package.writestr(folder + '/' + item['name'], b'')
    return zip_buffer.getvalue()


def get_user_shops(company_id, user_id):
    shops = Shop.objects.getList(company_id, 1, 1000) or []
    user_shops = UserShop.objects.getList(user_id, 1, 1000) or []
    shop_ids = set([item['shop_id'] for item in user_shops])
    return [shop for shop in shops if shop['id'] in shop_ids]


def get_user_permissions(user_id):
    user = User.objects.find(user_id)
    permissions = Permission.objects.getList(user['role_id'], 1, 1000) or []
    return set([item['permission'] for item in permissions])


def build_good_export_rows(shop_id):
    goods = Good.objects.getAll(shop_id) or []
    goods = sorted(goods, key=good_id_sort_key)
    aliases = GoodAlias.objects.getAllByShop(shop_id) or []
    follows = GoodFollow.objects.getAllByShop(shop_id) or []
    alias_map = {}
    for alias in aliases:
        good_id = alias['good_id']
        if good_id not in alias_map:
            alias_map[good_id] = []
        alias_map[good_id].append(alias['name'])

    follow_map = {}
    for follow in follows:
        follow_map[follow['good_id']] = follow['priority']

    rows = [GOOD_EXPORT_HEADERS]
    for good in goods:
        good_aliases = alias_map.get(good['good_id'], [])
        if len(good_aliases) > 5:
            raise ValueError('商品别名超过5个:' + good['good_id'] + ',' + good['short_name'])
        rows.append([
            good['short_name'],
            good['good_id'],
            follow_map.get(good['good_id'], 0),
            GoodType.num2text(good['good_type']),
            GoodStatus.num2text(good['good_status']),
            good['origin'],
            GoodOriginType.num2text(good['origin_type']),
            good['stock'],
            GoodStockType.num2text(good['stock_type']),
            good['name'],
            good_aliases[0] if len(good_aliases) > 0 else '',
            good_aliases[1] if len(good_aliases) > 1 else '',
            good_aliases[2] if len(good_aliases) > 2 else '',
            good_aliases[3] if len(good_aliases) > 3 else '',
            good_aliases[4] if len(good_aliases) > 4 else ''
        ])
    return rows


def build_xlsx(rows):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as workbook:
        workbook.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
        workbook.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        workbook.writestr('xl/workbook.xml', '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="商品" sheetId="1" r:id="rId1"/></sheets></workbook>')
        workbook.writestr('xl/_rels/workbook.xml.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        workbook.writestr('xl/worksheets/sheet1.xml', build_sheet_xml(rows))
    return output.getvalue()


def build_sheet_xml(rows):
    row_xml = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        for col_index, value in enumerate(row, start=1):
            ref = column_name(col_index) + str(row_index)
            text = escape('' if value is None else str(value))
            cells.append('<c r="' + ref + '" t="inlineStr"><is><t>' + text + '</t></is></c>')
        row_xml.append('<row r="' + str(row_index) + '">' + ''.join(cells) + '</row>')
    return '<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + ''.join(row_xml) + '</sheetData></worksheet>'


def column_name(index):
    name = ''
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def safe_zip_name(name):
    return str(name).replace('\\', '_').replace('/', '_')


def good_id_sort_key(good):
    good_id = str(good['good_id'])
    return (len(good_id), good_id)
