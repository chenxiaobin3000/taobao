chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || message.type !== 'download') {
    return false
  }
  chrome.downloads.download({
    url: message.url,
    filename: message.filename,
    conflictAction: 'overwrite',
    saveAs: false
  }, downloadId => {
    if (chrome.runtime.lastError) {
      sendResponse({ ok: false, message: chrome.runtime.lastError.message })
      return
    }
    sendResponse({ ok: true, id: downloadId })
  })
  return true
})
