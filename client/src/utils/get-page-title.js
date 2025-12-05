import defaultSettings from '@/settings'

const title = defaultSettings.title || '创想酷玩'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
