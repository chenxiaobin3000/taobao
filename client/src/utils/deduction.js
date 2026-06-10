import { DefaultOrder, DeductionType, FinanceType } from '@/utils/const'
import { excelDateToText } from '@/utils/excel'

export function extractOrderProcure(note, id, onLog) {
  const ret = [false, -1, '']
  if (note === undefined) {
    return [true, 0, DefaultOrder]
  }
  let count = 0
  const notes = String(note).split('|')
  for (let i = 0; i < notes.length; ++i) {
    if (notes[i].length > 19) {
      ++count
    }
  }
  if (count > 2 && note.indexOf('元-利润:0元') === -1 && note.indexOf('元 利润:0元') === -1) {
    writeLog(onLog, `未经过人工校验: ${id},${note}`)
    return ret
  }
  const data = notes[0].trim()
  if (data.length < 20) {
    return ret
  }
  const first = data.indexOf(':')
  if (first === -1) {
    writeLog(onLog, `没有找到账号信息: ${id},${note}`)
    return ret
  }
  const second = data.indexOf('-采购价:', first + 1)
  if (second === -1 || second - first !== 20) {
    writeLog(onLog, `没有找到-采购价: ${id},${note}`)
    return ret
  }
  let third = data.indexOf('元-利润:', second + 5)
  if (third === -1) {
    third = data.indexOf('元 利润:', second + 5)
  }
  if (third === -1) {
    writeLog(onLog, `没有找到利润信息: ${id},${note}`)
    return ret
  }
  ret[0] = true
  ret[1] = data.substring(second + 5, third)
  ret[2] = data.substring(first + 1, second)
  return ret
}

function writeLog(onLog, message) {
  if (onLog) {
    onLog(message)
  }
}

export function parseDeductionRows(results, columns, moduleName = '扣费') {
  const records = []
  results.forEach((row, index) => {
    if (row[columns.amount] <= 0) {
      return
    }
    const ftype = FinanceType.text2num(row[columns.financeType])
    if (ftype === FinanceType.PUBLIC) {
      return
    }
    const parsed = parseDeductionNote({
      financeType: ftype,
      note: row[columns.deductionNote],
      goodName: row[columns.goodName],
      rowIndex: index,
      moduleName
    })
    records.push({
      o: parsed.orderId,
      f: ftype,
      a: row[columns.amount],
      t: parsed.deductionType,
      c: excelDateToText(row[columns.createTime]),
      n: parsed.note
    })
  })
  records.forEach((record, index) => {
    if (record.t === DeductionType.OTHER || record.o.length !== 19) {
      throw new Error(`${moduleName}第${index + 2}行数据异常`)
    }
  })
  return records
}

export function parseDeductionNote({ financeType, note, goodName, rowIndex = 0, moduleName = '扣费' }) {
  let text = note || ''
  let deductionType = DeductionType.OTHER
  if (text.length < 2) {
    if (financeType === FinanceType.ONLINE) {
      deductionType = DeductionType.ONLINE
      text = goodName
    } else {
      throw new Error(`${moduleName}第${rowIndex + 2}行没有备注信息`)
    }
  } else if (financeType === FinanceType.TRANSFER && text === '收款') {
    deductionType = DeductionType.ZHUAN_ZHANG
    text = '刷单'
  } else {
    deductionType = DeductionType.text2num(text)
  }
  return {
    note: text,
    deductionType,
    orderId: extractDeductionOrderId(deductionType, text, rowIndex, moduleName)
  }
}

export function extractDeductionOrderId(deductionType, note, rowIndex = 0, moduleName = '扣费') {
  switch (deductionType) {
    case DeductionType.FU_WU_FEI:
    case DeductionType.XIN_XIANG:
    case DeductionType.XIN_KE:
    case DeductionType.TAO_JIN_BI:
    case DeductionType.XIAN_YONG_HOU_FU:
    case DeductionType.KUA_JING_JI_CHU:
    case DeductionType.KUA_JING_DA_JIAN:
    case DeductionType.TAO_TE:
    case DeductionType.XIAN_SHI:
    case DeductionType.XIN_PIN:
    case DeductionType.XIN_XIANG_FU_WU:
    case DeductionType.XIAO_FEI_QUAN:
    case DeductionType.GUAN_KONG:
    case DeductionType.XIAN_SHI_LI_JIN:
      return extractBetweenParentheses(note, rowIndex, moduleName)
    case DeductionType.TI_YAN:
      return extractAfter(note, '订单号', rowIndex, moduleName)
    case DeductionType.XIAN_YONG_TIAO_ZHANG:
      return extractBetweenParentheses(note, rowIndex, moduleName)
    case DeductionType.KUA_JING_ZENG_ZHI:
      return extractCrossBorderOrderId(note, rowIndex, moduleName)
    case DeductionType.JI_YUN_WU_LIU:
    case DeductionType.JI_YUN_CAO_ZUO_FEI:
      return extractAfter(note, '交易单号：', rowIndex, moduleName)
    case DeductionType.GONG_YI:
    case DeductionType.YAN_CHI_FA_HUO:
    case DeductionType.XU_JIA_FA_HUO:
    case DeductionType.WU_LIU_YI_CHANG:
    case DeductionType.QUE_HUO:
    case DeductionType.HUA_BEI:
    case DeductionType.WU_LIU_CHAO_SHI:
    case DeductionType.YAN_CHI_HUAN_HUO:
    case DeductionType.TUI_KUAN:
    case DeductionType.ZHUAN_ZHANG:
    case DeductionType.BAO_ZHENG_JIN:
    case DeductionType.DA_KUAN:
    case DeductionType.CHONG_ZHI:
    case DeductionType.ONLINE:
      return DefaultOrder
    default:
      throw new Error(`${moduleName}第${rowIndex + 2}行备注信息异常`)
  }
}

function extractBetweenParentheses(note, rowIndex, moduleName) {
  const key = note.indexOf('(KY_ITEM)')
  const first = key === -1 ? note.indexOf('(') + 1 : note.indexOf('(', key + 1) + 1
  const second = note.indexOf(')', first)
  if (first !== -1 && second !== -1 && second - first === 19) {
    return note.substring(first, second)
  }
  throw new Error(`${moduleName}第${rowIndex + 2}行备注格式异常`)
}

function extractAfter(note, keyword, rowIndex, moduleName) {
  const first = note.indexOf(keyword)
  if (first !== -1) {
    return note.substring(first + keyword.length, first + keyword.length + 19)
  }
  throw new Error(`${moduleName}第${rowIndex + 2}行备注格式异常`)
}

function extractCrossBorderOrderId(note, rowIndex, moduleName) {
  const first = note.indexOf('(') + 1
  let second = note.indexOf('_', first)
  if (first !== -1 && second !== -1 && second - first === 19) {
    return note.substring(first, second)
  }
  second = note.indexOf(')', first)
  if (first !== -1 && second !== -1 && second - first === 19) {
    return note.substring(first, second)
  }
  throw new Error(`${moduleName}第${rowIndex + 2}行备注格式异常`)
}
