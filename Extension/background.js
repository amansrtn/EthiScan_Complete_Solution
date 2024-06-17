var originalXHROpen = window.XMLHttpRequest.prototype.open;

window.XMLHttpRequest.prototype.open = function (method, url) {
    console.log('Outgoing request intercepted:', method, url);

    if (method.toUpperCase() === 'POST') {
        console.log('POST Data:', this._postData);
        console.log('Request Headers:', this._requestHeaders);
        console.log('Cookies:', document.cookie);
    }

    return originalXHROpen.apply(this, arguments);
};

chrome.webRequest.onBeforeRequest.addListener(
    function (details) {
        if (details.method === 'POST') {



            // console.log('Outgoing POST request intercepted (onBeforeRequest):', details);

            var payload = decodeURIComponent(String.fromCharCode.apply(null, new Uint8Array(details.requestBody.raw[0].bytes)));

            if (details.requestBody && details.requestBody.raw) {
                var detailsapi = { 'Request details: ': details, 'Request Payload:': payload }

                console.log(detailsapi);
                if (payload.toLowerCase().includes('pass')) {
                    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                        chrome.tabs.sendMessage(tabs[0].id, { type: 'apiCall', siteurl: details.url });
                    });
                }
            }
        }
        return { cancel: false };
    },
    { urls: ["<all_urls>"] },
    ["blocking", "requestBody"]
);

// chrome.webRequest.onBeforeSendHeaders.addListener(
//   function(details) {
//       if (details.method === 'POST') {
//           console.log('Outgoing POST request intercepted (onBeforeSendHeaders):', details);

//           // Accessing request headers
//           if (details.requestHeaders) {
//               console.log('Request Headers:', details.requestHeaders);
//           }
//       }
//       return { requestHeaders: details.requestHeaders };
//   },
//   { urls: ["<all_urls>"] },
//   ["blocking", "requestHeaders"]
// );

chrome.runtime.onInstalled.addListener(function () {
    chrome.contextMenus.create({
      title: "Report Text",
      contexts: ["selection"],
      id: "reportText"
    });
  });
  
  chrome.contextMenus.onClicked.addListener(function (info, tab) {
    if (info.menuItemId === "reportText") {
      chrome.tabs.sendMessage(tab.id, { action: "reportText", selectedText: info.selectionText });
    }
  });
  