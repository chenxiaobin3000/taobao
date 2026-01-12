/**
 * excel 时间转换
 * @param {int} xlsx_time
 * @returns {string}
 */
export function xlsx_time_str(xlsx_date) {
  const date = new Date((xlsx_date - 2) * 24 * 3600000 + 1 - 8 * 3600000)
  const Y = (date.getFullYear() - 70) + '-'
  const M = (date.getMonth() + 1) + '-'
  const D = date.getDate() + ' '
  const h = date.getHours() + ':'
  const m = date.getMinutes() + ':'
  const s = date.getSeconds()
  return Y + M + D + h + m + s
}

/**
 * excel 日期转换
 * @param {int} xlsx_date
 * @returns {string}
 */
export function xlsx_date_str(xlsx_date) {
  const date = new Date((xlsx_date - 2) * 24 * 3600000 + 1 - 8 * 3600000)
  const Y = (date.getFullYear() - 70) + '-'
  const M = (date.getMonth() + 1) + '-'
  const D = date.getDate()
  return Y + M + D
}
