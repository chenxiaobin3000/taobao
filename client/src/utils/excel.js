/**
 * 将 Excel 日期转为文本，时区固定为 Asia/Shanghai
 * 支持：
 * - Excel 序列号日期，如 45658
 * - JS Date 对象
 * - 可被 Date 解析的字符串
 */
export function excelDateToText(value, format = 'yyyy-MM-dd HH:mm:ss') {
  if (value === null || value === undefined || value === '') {
    return ''
  }

  let date

  // Excel 日期序列号：以 1899-12-30 为基准
  if (typeof value === 'number') {
    const utcDays = value - 25569
    const utcMs = utcDays * 86400 * 1000
    date = new Date(utcMs)
  } else if (value instanceof Date) {
    date = value
  } else {
    date = new Date(value)
  }

  if (Number.isNaN(date.getTime())) {
    return String(value)
  }

  const parts = new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).formatToParts(date)

  const map = {}
  parts.forEach(part => {
    map[part.type] = part.value
  })

  return format
    .replace('yyyy', map.year)
    .replace('MM', map.month)
    .replace('dd', map.day)
    .replace('HH', map.hour)
    .replace('mm', map.minute)
    .replace('ss', map.second)
}
