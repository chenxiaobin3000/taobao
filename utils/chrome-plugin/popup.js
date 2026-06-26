const SHOP_LIST = [
  { id: 1, name: '德国KSTE' },
  { id: 2, name: '挪威VER' },
  { id: 3, name: '日本SKLA' },
  { id: 5, name: '法国FALS' },
  { id: 4, name: '酷娃KUWA' }
]

const shopIdSelect = document.getElementById('shopId')
const saveButton = document.getElementById('save')
const statusEl = document.getElementById('status')

initShopSelect()

chrome.storage.local.get(['shopId'], data => {
  const shopId = data.shopId || String(SHOP_LIST[0].id)
  shopIdSelect.value = shopId
})

shopIdSelect.addEventListener('change', () => {
  chrome.storage.local.set({ shopId: shopIdSelect.value })
})

saveButton.addEventListener('click', async() => {
  setStatus('处理中...')
  saveButton.disabled = true
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
    if (!tab || !tab.id || !tab.url) {
      throw new Error('未找到当前页面')
    }
    const itemId = getItemId(tab.url)
    if (!itemId) {
      throw new Error('当前链接没有商品ID')
    }
    const [{ result }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: extractImageUrl
    })
    if (!result) {
      throw new Error('未识别到商品图片')
    }
    const shopId = shopIdSelect.value
    const filename = 'good_images/' + shopId + '/' + itemId + getImageExt(result)
    await chrome.runtime.sendMessage({
      type: 'download',
      url: result,
      filename
    })
    setStatus('已保存: ' + filename)
  } catch (error) {
    setStatus(error.message || String(error))
  } finally {
    saveButton.disabled = false
  }
})

function initShopSelect() {
  shopIdSelect.innerHTML = ''
  SHOP_LIST.forEach(shop => {
    const option = document.createElement('option')
    option.value = String(shop.id)
    option.textContent = shop.name
    shopIdSelect.appendChild(option)
  })
}

function setStatus(text) {
  statusEl.textContent = text
}

function getItemId(url) {
  try {
    const data = new URL(url)
    return data.searchParams.get('id') || data.searchParams.get('itemId') || ''
  } catch (error) {
    return ''
  }
}

function getImageExt(url) {
  const cleanUrl = url.split('?')[0]
  const match = cleanUrl.match(/\.(jpg|jpeg|png|webp)(?:_|$)/i)
  if (!match) {
    return '.jpg'
  }
  const ext = match[1].toLowerCase()
  return ext === 'jpeg' ? '.jpg' : '.' + ext
}

function extractImageUrl() {
  const meta = document.querySelector('meta[property="og:image"], meta[name="og:image"]')
  if (meta && meta.content) {
    return normalizeUrl(meta.content)
  }

  const scripts = Array.from(document.scripts).map(script => script.textContent || '').join('\n')
  const scriptMatch = scripts.match(/(?:picUrl|pic_url|mainPic|image)["']?\s*[:=]\s*["']([^"']+alicdn\.com[^"']+)["']/i)
  if (scriptMatch) {
    return normalizeUrl(scriptMatch[1])
  }

  const imgs = Array.from(document.images)
    .map(img => ({
      src: img.currentSrc || img.src,
      area: (img.naturalWidth || img.width || 0) * (img.naturalHeight || img.height || 0)
    }))
    .filter(item => item.src && item.src.indexOf('alicdn.com') !== -1)
    .filter(item => !/sprite|logo|avatar|icon|loading/i.test(item.src))
    .sort((a, b) => b.area - a.area)
  return imgs.length > 0 ? normalizeUrl(imgs[0].src) : ''

  function normalizeUrl(url) {
    url = String(url || '').replace(/\\\//g, '/')
    if (url.indexOf('//') === 0) {
      return location.protocol + url
    }
    return url
  }
}
