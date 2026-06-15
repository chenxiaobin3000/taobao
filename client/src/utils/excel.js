const PROJECT_TIME_ZONE = 'Asia/Shanghai'
const DAY_MS = 24 * 60 * 60 * 1000
const EXCEL_EPOCH_UTC = Date.UTC(1899, 11, 30)

function pad(num) {
  return String(num).padStart(2, '0')
}

function formatParts(parts, format) {
  return format
    .replace('yyyy', parts.year)
    .replace('MM', parts.month)
    .replace('dd', parts.day)
    .replace('HH', parts.hour)
    .replace('mm', parts.minute)
    .replace('ss', parts.second)
}

function getDatePartsInProjectTimeZone(date) {
  const parts = new Intl.DateTimeFormat('zh-CN', {
    timeZone: PROJECT_TIME_ZONE,
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
  return map
}

function getExcelSerialParts(value) {
  const serialMs = Math.round(value * DAY_MS)
  const date = new Date(EXCEL_EPOCH_UTC + serialMs)
  return {
    year: String(date.getUTCFullYear()),
    month: pad(date.getUTCMonth() + 1),
    day: pad(date.getUTCDate()),
    hour: pad(date.getUTCHours()),
    minute: pad(date.getUTCMinutes()),
    second: pad(date.getUTCSeconds())
  }
}

function getTextDateParts(value) {
  const match = String(value).trim().match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})(?:[ T](\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?/)
  if (!match) {
    return null
  }
  return {
    year: match[1],
    month: pad(match[2]),
    day: pad(match[3]),
    hour: pad(match[4] || 0),
    minute: pad(match[5] || 0),
    second: pad(match[6] || 0)
  }
}

export function excelDateToText(value, format = 'yyyy-MM-dd HH:mm:ss') {
  if (value === null || value === undefined || value === '') {
    return ''
  }

  if (typeof value === 'number') {
    return formatParts(getExcelSerialParts(value), format)
  }

  if (typeof value === 'string') {
    const parts = getTextDateParts(value)
    if (parts) {
      return formatParts(parts, format)
    }
  }

  const date = value instanceof Date ? value : new Date(value)
  if (Number.isNaN(date.getTime())) {
    return String(value)
  }

  return formatParts(getDatePartsInProjectTimeZone(date), format)
}
