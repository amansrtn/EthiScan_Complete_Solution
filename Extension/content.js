// content.js
// const extensionAPI = typeof browser === 'undefined' ? extensionAPI : browser;

function convertStringToNumber(inputString) {
  const rupeeIndex = inputString.indexOf('₹');

  // Extract the substring after the rupee symbol
  const substringAfterRupee = rupeeIndex !== -1 ? inputString.substring(rupeeIndex + 1) : inputString;

  // Remove non-digit characters, except for dots and commas
  const cleanedString = substringAfterRupee.replace(/[^\d.,]/g, '');

  // Replace commas with empty string to handle thousand separators
  const stringWithoutCommas = cleanedString.replace(/,/g, '');

  // Find the first occurrence of a valid numeric sequence
  const match = stringWithoutCommas.match(/\d+(\.\d+)?/);

  // If a match is found, convert it to a number; otherwise, return NaN
  const result = match ? parseFloat(match[0]) : NaN;

  return result;
}

function extractSiteName(url) {
  let cleanedUrl = url.replace(/^(https?:\/\/)?(www\.)?/, '');

  let match = cleanedUrl.match(/^([^\/\.]+)/);

  return match ? match[0] : null;
}

function getCheckoutPrice() {
  const priceElements = document.querySelectorAll('body :not(script):not(style)'); // Exclude scripts and styles
  let extractedPrice = null;
  let maxFont = -1;
  priceElements.forEach(element => {
    const textContent = element.textContent.trim();
    if ((textContent.includes("Total")) || textContent.includes("total") || textContent.includes("Subtotal")) {
      let nextSibling = element.nextElementSibling;
      if (nextSibling) {
        let nextContent = nextSibling.textContent.trim();
        if (/\d/.test(nextContent)) {
          extractedPrice = nextContent;
        }

      }

    }
  });
  return extractedPrice;
}

var found = 0;
chrome.storage.local.set({ "depth": 0 })
let style = document.createElement('style');
style.textContent = `
    *[button-highlighted="true"] {
      background-color: rgba(0,255,0,.4) !important;
      border: 5px solid green !important;
    }
  `;
document.head.appendChild(style);

function isPriceText(text) {

  return text.includes("₹");
}
// Function to extract price from the webpage

function extractPrice1() {
  const priceElements = document.querySelectorAll('body :not(script):not(style)'); // Exclude scripts and styles
  let extractedPrice = null;
  let maxFont = -1;
  priceElements.forEach(element => {
    const fontSize = window.getComputedStyle(element).fontSize;
    const textContent = element.textContent.trim();

    const numfontSize = parseInt(fontSize, 10);
    if (textContent.includes("₹") || textContent.includes("Rs")) {
      if (maxFont < numfontSize) {
        extractedPrice = textContent.toString();
        maxFont = numfontSize;
      }
      //extractedPrice = textContent;
    }
  });

  let cleanExtractedPrice = convertStringToNumber(extractedPrice);
  console.log("before: ", cleanExtractedPrice);
  extensionAPI.storage.local.set({ key: cleanExtractedPrice }, function () {
  });
}

// Run the extraction when the extension icon is clicked
extensionAPI.runtime.onMessage.addListener(

  function (request, sender, sendResponse) {
    if (request.action === "extractPrice") {
      extractPrice();
      extensionAPI.storage.local.get(['key'], function (result) {
        extensionAPI.runtime.sendMessage({ price: result.key });
      });
    }
    else if (request.action === "scanButtons") {
      scanButtons();
    }
    else if (request.action === "calcDiff") {
      try {
        let priceDuringCheckOut = getCheckoutPrice();

        let cleanedPriceDuringCheckout = convertStringToNumber(priceDuringCheckOut);
        console.log("after: ", cleanedPriceDuringCheckout)
        extensionAPI.storage.local.get(['delivery'], function (delchrg) {


          console.log("-------------", delchrg.delivery);
          extensionAPI.storage.local.get(['key'], function (result) {
            let val = parseInt(result.key);
            let delv = parseInt(delchrg.delivery);
            let diff = cleanedPriceDuringCheckout - val - delv;
            if (diff === 0) {
              diff = "0";
            }
            extensionAPI.runtime.sendMessage({ price: diff });
          });
        });
      } catch (error) {
        console.log(error)
      }
    }

    else if(request.action=='tnccheck'){
      
        let links = Array.from(document.links);
        links.forEach(function (link) {
          let href = link.href;
          // var s = extractSiteName(href);
          // let url = new URL(href);
          let linktitle = link.innerText;
          if (href.toLowerCase().includes('terms') || linktitle.toLowerCase().includes('terms')) {
            const apiurl = 'http://127.0.0.1:8000/tncanalyzer/';
            fetch(apiurl, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ "link": href }),
            })
              .then((resp) => resp.json())
              .then((data) => {
                console.log(data.text)
                json = data;
                var res=data.text.toString()
                alert(res);
                sendResponse({'tncdata':res});
              })
              .catch((error) => {
                console.log(error);
              });
          }
        });
      
    }

    else if (request.action === 'scanLinks') {
      let links = Array.from(document.links);
      let storedLinks = {};

      extensionAPI.storage.local.get('links', function (result) {
        storedLinks = result.links || {};
        links.forEach(function (link) {
          let href = link.href;
          if (href.toLowerCase().indexOf('/p/'.toLowerCase()) !== -1) {
            storedLinks[href] = (storedLinks[href] || 0) + 1;
          }
          else if (href.toLowerCase().indexOf('/dp/'.toLowerCase()) !== -1) {
            storedLinks[href] = (storedLinks[href] || 0) + 1;
          }
        });

        // Save updated links to extensionAPI storage
        extensionAPI.storage.local.set({ 'links': storedLinks }, function () {
          console.log('Links scanned and stored:', storedLinks);
        });
      });
    }
    else if (request.action === 'findHighestLink') {
      sendResponse(findHighestLink())
    }
  }

);


function extractPrice() {
  extractPrice1();
  extensionAPI.storage.local.get(['key'], function (result) {
    console.log("extracted price:", result.key)

    extensionAPI.runtime.sendMessage({ price: result.key });
  });
}


function calcDiff() {
  var currentURL = window.location.href;
  if ((currentURL.toLowerCase().indexOf('/buy/'.toLowerCase()) !== -1) || (currentURL.toLowerCase().indexOf('/cart'.toLowerCase()) !== -1) || (currentURL.toLowerCase().indexOf('/checkout/'.toLowerCase()) !== -1)) {
    try {
      let priceDuringCheckOut = getCheckoutPrice();

      let cleanedPriceDuringCheckout = convertStringToNumber(priceDuringCheckOut);
      console.log("after: ", cleanedPriceDuringCheckout)
      extensionAPI.storage.local.get(['delivery'], function (delchrg) {


        console.log("-------------", delchrg.delivery);
        extensionAPI.storage.local.get(['key'], function (result) {
          let val = parseInt(result.key);
          let delv = parseInt(delchrg.delivery);
          let diff = cleanedPriceDuringCheckout - val - delv;
          if (diff === 0) {
            diff = "0";
          }
          if (diff > 0 && diff < 1000) {
            extensionAPI.storage.local.set({ 'hiddencost': diff.toString() });
            alert("There is hidden cost of: " + diff.toString());
          }
          console.log("price difference:", diff)
          extensionAPI.runtime.sendMessage({ price: diff });
        });
      });
    } catch (error) {
      console.log(error)
    }

  }
  // let priceDuringCheckOut = getCheckoutPrice();
  // let cleanedPriceDuringCheckout = convertStringToNumber(priceDuringCheckOut);
  // extensionAPI.storage.local.get(['key'], function (result) {
  //   let val = parseInt(result.key);
  //   let diff = cleanedPriceDuringCheckout - val;
  //   if (diff === 0) {
  //     diff = "0";
  //   }

  //   console.log("price difference:", diff)
  //   extensionAPI.runtime.sendMessage({ price: diff });
  // });
}


function scanLinks() {
  try {
    let links = Array.from(document.links);
    let storedLinks = {};
    // let checked = ["example"];
    let style = document.createElement('style');
    style.textContent = `
    a[data-highlighted="true"] {
      background-color: rgba(255,247,0,.6) !important;
      border: 5px solid red !important;
    }
  `;

    document.head.appendChild(style);

    extensionAPI.storage.local.get('links', function (result) {
      storedLinks = result.links || {};
      links.forEach(function (link) {
        let href = link.href;
        // var s = extractSiteName(href);
        // let url = new URL(href);
        let linktitle = link.innerText;

        // if (href.toLowerCase().includes('terms') || linktitle.toLowerCase().includes('terms')) {
        //   const apiurl = 'http://127.0.0.1:8000/tncanalyzer/';
        //   fetch(apiurl, {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify({ "link": href }),
        //   })
        //     .then((resp) => resp.json())
        //     .then((data) => {
        //       console.log(data)
        //       json = data;

        //       extensionAPI.storage.local.set({tncdata:json.text})
        //     })
        //     .catch((error) => {
        //       console.log(error);
        //     });
        // }

        // if (!(checked.includes(s))) {
        //   checked.push(s);
        //   const apiurl = 'http://127.0.0.1:8000/urlanalyzer/';
        //   fetch(apiurl, {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify({ "baseUrl": url.hostname() }),
        //   })
        //     .then((resp) => resp.json())
        //     .then((data) => {
        //       console.log(data)
        //       json = data;
        //       if (json.flag !== "False") {
        //         elements[i].setAttribute('data-highlighted', 'true');

        //       }
        //     })
        //     .catch((error) => {
        //       console.log(error);
        //     });
        // }
        if (href.toLowerCase().indexOf('/p/'.toLowerCase()) !== -1) {
          storedLinks[href] = (storedLinks[href] || 0) + 1;
        }
        else if (href.toLowerCase().indexOf('/dp/'.toLowerCase()) !== -1) {
          storedLinks[href] = (storedLinks[href] || 0) + 1;
        }
        else if (href.toLowerCase().indexOf('/buy'.toLowerCase()) !== -1) {
          storedLinks[href] = (storedLinks[href] || 0) + 1;
        }
      });

      // Save updated links to extensionAPI storage
      extensionAPI.storage.local.set({ 'links': storedLinks }, function () {
        console.log('Links scanned and stored:', storedLinks);
      });
    });
  } catch (e) {
    console.log(e);
  }
}





function findHighestLink() {
  extensionAPI.storage.local.get('links', function (result) {


    let style = document.createElement('style');
    style.textContent = `
    a[data-highlighted="true"] {
      background-color: rgba(255,247,0,.6) !important;
      border: 5px solid red !important;
    }
  `;

    document.head.appendChild(style);

    const storedLinks = result.links || {};
    let highestLink = null;
    let highestValue = 3;

    // Find the link with the highest value
    for (const [link, value] of Object.entries(storedLinks)) {
      if (value > highestValue) {
        highestLink = link;
        highestValue = value;
      }
    }

    if (highestLink !== null) {
      console.log('Link with the highest value:', highestLink, 'with value:', highestValue);
      extensionAPI.runtime.sendMessage({ nagginglink: highestLink })
      // alert('Link with the highest value:\n' + highestLink + '\nwith value: ' + highestValue);
    } else {
      console.log('No links found in storage.');
      // alert('No links found in storage.');
    }

    let links = Array.from(document.links);
    for (let i = 0; i < links.length; i++) {

      if (links[i].href === highestLink) {
        links[i].setAttribute('data-highlighted', 'true');
        return highestLink;

      } else {
        links[i].removeAttribute('data-highlighted');
      }
    }

  });
}

function darkpcount() {
  const darkPatternElements = document.querySelectorAll('[dark-pattern]');
  const darkPatterns = {};

  darkPatternElements.forEach(function (element) {
    const value = element.getAttribute('dark-pattern');
    if (value in darkPatterns) {
      darkPatterns[value]++;
    } else {
      darkPatterns[value] = 1;
    }
  });

  const darkPatternst = {};
  try {
    for (let value in darkPatterns) {
      darkPatternst[value] = [];
      console.log((value.replace(" ", "-")).toString().toLowerCase());
      const s = "[" + value.replace(" ", "-").toString().toLowerCase() + "]"
      const darkPatterntypes = document.querySelectorAll(s);
      console.log(darkPatterntypes)

      darkPatterntypes.forEach(function (element) {
        const value1 = element.getAttribute(value.replace(" ", "-").toString());
        console.log(value1)
        darkPatternst[value].push(value1)
      });
    }
  } catch (error) {
    console.log(error)
  }
  console.log(darkPatternst);

  return darkPatternst;

}

extensionAPI.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'performdarkdisplay') {
    var result = darkpcount();
    sendResponse(result);
  }
});

extensionAPI.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'clearCheckbox') {
    try {
      const checkboxes = document.querySelectorAll('input[type="checkbox"]');
      checkboxes.forEach((checkbox) => {
        checkbox.checked = false;
      })
      sendResponse('Done');
    } catch (error) {
      sendResponse(error);
    }
  }
});

let checked = ["example"];
var curnum = 0;
let darkpat = {}
function scantexts() {

  let currentDomain = document.domain;
  let currentTitle = extractSiteName(document.domain);
  console.log(currentDomain)


  let elements = segments(document.body);
  let filtered_elements = [];

  var isprodpage = checkprodpage();

  extensionAPI.storage.local.set({ 'darksentence': [] });

  let style = document.createElement('style');
  style.textContent = `
    *[data-highlighted="true"] {
      position: relative;
      background-color: rgba(154,210,67,.8);
      border: 3px solid red !important;
    }
    .highlighted-text {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      background-color: white;
      border: 1px solid black;
      padding: 5px;
      z-index: 999;
      overflow: visible !important;
      /* Add any other styling for the highlighted text box */
    }
    *[data-highlighted="true"]:hover .highlighted-text {
      display: block;
    }
  `;

  document.head.appendChild(style);

  var x = 0;
  var t = 0;
  var u = 0;
  var ch = 0;
  for (let i = 0; i < elements.length; i++) {
    if (!(elements[i] && elements[i].innerText)) {
      continue;
    }



    let text = elements[i].innerText.trim().replace(/\t/g, " ");

    if (text.length == 0 || text == null || text.length > 200) {
      continue;
    }

    if (text in darkpat) {
      // let highlightedText = document.createElement('span');
      // highlightedText.className = 'highlighted-text';
      // // highlightedText.textContent = '(' + repeat + ')';
      // // highlightedText.style.overflow = 'visible';
      // elements[i].style.overflow = 'visible';


      // let highlightedText = document.createElement('span');
      // highlightedText.textContent = '('+json.pattern+')';

      elements[i].setAttribute('data-highlighted', 'true');

      // elements[i].appendChild(highlightedText);

      if (darkpat[text] == "high") {
        elements[i].setAttribute("style", "background-color: rgba(255,247,0,.6)")
      }

      // elements[i].setAttribute('dark-pattern', (json.pattern).toString())

      // elements[i].setAttribute((json.pattern).toString().replace(" ", "-"), text)
    }

    if ((text.toLowerCase().includes('ends in') || text.toLowerCase().includes('offer ends') || text.toLowerCase().includes('time remaining')) && ch == 0) {

      u = 1;
      ch = 1;
      if (/\d/.test(text)) {
        u = 0;
        var tdata = text + "$$$$";
        console.log(JSON.stringify({ "text": tdata, "webName": currentTitle, "baseUrl": currentDomain, "prodName": document.title, "isProdPage": isprodpage.toString(), "count": ++curnum }))

        const apiurl = 'http://127.0.0.1:8000/txtanalyzer/'
        fetch(apiurl, {
          method: "POST",
          mode: 'cors',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ "text": tdata, "webName": currentTitle, "baseUrl": currentDomain, "prodName": document.title, "isProdPage": isprodpage.toString(), "count": ++curnum }),
        })
          .then((resp) => resp.json())
          .then((data) => {
            json = data;
            if (json.flag == "true") {
              var level = json.level;
              console.log(text);
              extensionAPI.storage.local.get('darksentences', function (result) {
                var storageList = result.darksentences || [];
                storageList.push(text);
                extensionAPI.storage.local.set({ 'darksentences': storageList });

              });

              let highlightedText = document.createElement('span');
              highlightedText.className = 'highlighted-text';
              highlightedText.textContent = '(' + json.pattern + ')';
              highlightedText.style.overflow = 'visible';
              elements[i].style.overflow = 'visible';

              elements[i].setAttribute('data-highlighted', 'true');
              elements[i].appendChild(highlightedText);
              elements[i].setAttribute('dark-pattern', (json.pattern).toString())

              elements[i].setAttribute((json.pattern).toString().replace(" ", "-"), text)
              if (level == "high") {
                elements[i].setAttribute("style", "background-color: rgba(255,247,0,.6)")
              }

            }

          })
        continue;
      }
      continue;
    }
    else if (u == 1) {
      u = 0;
      var tdata = "Ends In $$$$ " + text;
      console.log(JSON.stringify({ "text": tdata, "webName": currentTitle, "baseUrl": currentDomain, "prodName": document.title, "isProdPage": isprodpage.toString(), "count": ++curnum }))
      const apiurl = 'http://127.0.0.1:8000/txtanalyzer/'
      fetch(apiurl, {
        method: "POST",
        mode: 'cors',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "text": tdata, "webName": currentTitle, "baseUrl": currentDomain, "prodName": document.title, "isProdPage": isprodpage.toString(), "count": ++curnum }),
      })
        .then((resp) => resp.json())
        .then((data) => {
          json = data;
          if (json.flag == "true") {
            var level = json.level;
            console.log(text);
            extensionAPI.storage.local.get('darksentences', function (result) {
              var storageList = result.darksentences || [];
              storageList.push(text);
              extensionAPI.storage.local.set({ 'darksentences': storageList });

            });

            let highlightedText = document.createElement('span');
            highlightedText.className = 'highlighted-text';
            highlightedText.textContent = '(' + json.pattern + ')';
            highlightedText.style.overflow = 'visible';
            elements[i].style.overflow = 'visible';

            elements[i].setAttribute('data-highlighted', 'true');
            elements[i].appendChild(highlightedText);
            elements[i].setAttribute('dark-pattern', (json.pattern).toString())

            elements[i].setAttribute((json.pattern).toString().replace(" ", "-"), text)
            if (level == "high") {
              elements[i].setAttribute("style", "background-color: rgba(255,247,0,.6)")
            }

          }

        })
      continue;
    }

    if (text.toLowerCase().includes('order placed') || text.toLowerCase().includes('order has been placed') || text.toLowerCase().includes('order successfully placed') || text.toLowerCase().includes('order confirmed')) {
      extensionAPI.storage.local.get(['latestProdName'], function (result) {
        var prodName = result.latestProdName;

        const apiurl = 'http://127.0.0.1:8000/txtanalyzer/update/'
        fetch(apiurl, {
          method: "POST",
          mode: 'cors',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ "baseUrl": currentDomain, "prodName": prodName }),
        })
      });
      checked.push(text);
      continue
    }
    else if (text.toLowerCase().includes('delivery charge') && ch == 0) {
      t = 1;
      ch = 1;
    }
    else if (t == 1) {
      try {
        console.log("===================---------", text);
        var remcst = convertStringToNumber(text)
        console.log("===================", remcst);
        t = 0;
        extensionAPI.storage.local.set({ "delivery": remcst })

      } catch (error) {
        console.log(error)
      }
    }
    if (!(checked.includes(text))) {
      checked.push(text)
      filtered_elements.push(text);
      console.log(text)
      if ((text.toLowerCase() == "out of stock" || text.toLowerCase() == "this item is sold out") && x == 0) {
        if (confirm("Were you advertised for this product") == true) {
          elements[i].setAttribute('data-highlighted', 'true');
          x = 1;
        } else {
          x = 0;
        }
      }
      const apiurl = 'http://127.0.0.1:8000/txtanalyzer/'
      fetch(apiurl, {
        method: "POST",
        mode: 'cors',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "text": text, "webName": currentTitle, "baseUrl": currentDomain, "prodName": document.title, "isProdPage": isprodpage.toString(), "count": ++curnum }),
      })
        .then((resp) => resp.json())
        .then((data) => {
          // console.log(data, text)
          json = data;
          if (json.flag == "true") {
            var level = json.level;
            console.log(text);
            extensionAPI.storage.local.get('darksentences', function (result) {
              var storageList = result.darksentences || [];
              storageList.push(text);
              extensionAPI.storage.local.set({ 'darksentences': storageList });

            });
            let highlightedText = document.createElement('span');
            highlightedText.className = 'highlighted-text';
            highlightedText.textContent = '(' + json.pattern + ')';
            highlightedText.style.overflow = 'visible';
            elements[i].style.overflow = 'visible';


            // let highlightedText = document.createElement('span');
            // highlightedText.textContent = '('+json.pattern+')';

            elements[i].setAttribute('data-highlighted', 'true');
            elements[i].appendChild(highlightedText);
            elements[i].setAttribute('dark-pattern', (json.pattern).toString())

            elements[i].setAttribute((json.pattern).toString().replace(" ", "-"), text)
            if (level == "high") {
              elements[i].setAttribute("style", "background-color: rgba(255,247,0,.6)")
            }
            darkpat[text] = level;


          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }
  console.log(filtered_elements);
}

function checkprodpage() {
  try {
    var pagetitle = document.title.toLowerCase().split(/\s+/);
    var url = window.location.href;
    console.log(pagetitle, url);
    url = url.split('?')[0];
    var cnt = 0;

    pagetitle.forEach((s) => {
      console.log(s);
      if (url.includes(s)) {
        cnt++;
      }
    })
    if (cnt >= 2) {
      extensionAPI.storage.local.set({ 'latestProdName': document.title })
      return true;
    }
    return false;
  } catch (error) {
    console.log(error);
  }

}


async function scanButtons() {
  try {
    if (found == 0) {
      const buttons = document.querySelectorAll('button');
      const links = Array.from(document.links);
      const atag = document.querySelectorAll('a');
      const buttonData = {};

      buttons.forEach(button => {
        const buttonText = button.innerText.trim().replace(/\t/g, " ");
        buttonData[buttonText.toLowerCase()] = button
      });
      links.forEach(link => {
        const linktext = link.innerText.trim().replace(/\t/g, " ");
        buttonData[linktext.toLowerCase()] = link;
      })
      atag.forEach(link => {
        const linktext = link.innerText.trim().replace(/\t/g, " ");
        buttonData[linktext.toLowerCase()] = link;
      })

      const postData = { buttons: buttonData }
      console.log(postData);

      const response = await fetch('http://127.0.0.1:8000/subtricky/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData),
      });
      const data = await response.json();
      var ele = buttonData[data.step.toLowerCase()];
      var fnd = data.found;
      if (fnd == "true") found = 1;

      extensionAPI.storage.local.get('depth', function (result) {
        chrome.storage.local.set({ "depth": result + 1 });
      });
      ele.setAttribute('button-highlighted', 'true');
      alert("Click on : "+ data.step.toString())
    }
    else {
      alert("button already found")
      extensionAPI.storage.local.get('depth', function (result) {

        const response = fetch('http://127.0.0.1:8000/depthofcancel/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(result),
        });
      });
    }
  } catch (e) {
    console.log(e);
  }

}
// var ele = document.getElementById('hhh';)
// var elementToHighlight = ele;

// if (elementToHighlight) {
//   var allElements = document.body.getElementsByTagName('*');
//   for (var i = 0; i < allElements.length; i++) {
//     if (allElements[i] !== elementToHighlight) {
//       allElements[i].style.filter = 'brightness(0.5)';
//     }
//   }

//   elementToHighlight.style.filter = 'brightness(1)';
// }


extensionAPI.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.type === 'apiCall') {
    let currentDomain = document.domain;
    if (!message.siteurl.includes(currentDomain)) {
      // alert(message.siteurl);
      console.log(message.siteurl)
    }
  }
});

window.addEventListener('beforeunload', function () {
  // extensionAPI.storage.local.clear(function () {
  //   console.log('browser storage cleared.');
  // });
});

let isChecking = false;
window.addEventListener('load', function () {

  this.setTimeout(() => { scantexts(); }, 1000);
  // scanButtons();
  // this.setTimeout(() => { scanButtons(); }, 15000)
  this.setTimeout(() => { darkpcount(); }, 10000);

  // scantexts();
  calcDiff();
  extractPrice();
  scanLinks();

  findHighestLink();
});

function handleChanges() {
  if (!isChecking) {
    isChecking = true;
    scantexts();
    darkpcount();

    checkprodpage();
    setTimeout(() => {
      isChecking = false;
    }, 5000);
  }

  calcDiff();
}

const observer = new MutationObserver(handleChanges);

const config = { childList: true, subtree: true };

observer.observe(document.body, config);

handleChanges();


chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "reportText") {

    reportText(request.selectedText);
  }
});

function reportText(selectedText) {
  console.log("Selected Text:", selectedText);
}
