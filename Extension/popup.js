// popup.js
const extensionAPI = typeof browser === 'undefined' ? chrome : browser;

document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('clearStorageButton').addEventListener('click', clearStorage);
    document.getElementById('clearCheckbox').addEventListener('click', clearcheckbox);
    document.getElementById('subscriptiontricky').addEventListener('click', subscriptiontricky);
    document.getElementById('termsncondition').addEventListener('click', termsncondition);

    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var activeTab = tabs[0];
        extensionAPI.tabs.sendMessage(activeTab.id, { action: 'findHighestLink' }, function (response) {
            var countele = document.getElementById('highlink');
            countele.textContent = response;
        });
    });

    extensionAPI.storage.local.get('darksentences', function (result) {

        storageList = result.darksentences || [];
        var dcount = storageList.length;
        var countele = document.getElementById('dkcount');
        countele.innerText = dcount;
        console.log(storageList);
        // var ul = document.getElementById('dksentence');

        // storageList.forEach(function (value, index) {
        //     var li = document.createElement('li');
        //     li.textContent = value;
        //     ul.appendChild(li);
        // });
        extensionAPI.storage.local.get('hiddencost', function (result) {

            if (result.hiddencost) {
                var elemen = document.getElementById('extdif');
                elemen.textContent = result.hiddencost;
            }

        });

    });
});

function termsncondition(){
    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var activeTab = tabs[0];
        extensionAPI.tabs.sendMessage(activeTab.id, { action: 'tnccheck' }, function (response) {
            console.log(response);
            
        });
    });
}

function subscriptiontricky(){
    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var activeTab = tabs[0];
        extensionAPI.tabs.sendMessage(activeTab.id, { action: 'scanButtons' }, function (response) {
            console.log(response)
        });
    });
}

function clearcheckbox(){
    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var activeTab = tabs[0];
        extensionAPI.tabs.sendMessage(activeTab.id, { action: 'clearCheckbox' }, function (response) {
            console.log(response)
        });
    });
}


document.addEventListener('DOMContentLoaded', function () {
    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var activeTab = tabs[0];
        extensionAPI.tabs.sendMessage(activeTab.id, { action: 'performdarkdisplay' }, function (response) {
            console.log('Response from content script:', response);

            var dcount = 0;
            

            dtcontainer = document.getElementById('dtype-container');

            for (let value in response) {
                dcount++;
                const faqItem = document.createElement('div');
                faqItem.className = 'py-5 shadow-xl';

                const details = document.createElement('details');
                details.className = 'group';

                const summary = document.createElement('summary');
                summary.className = 'flex p-2 justify-between items-center font-medium cursor-pointer list-none';
                summary.innerHTML = `
        <span>${value}</span>
        <span class="transition group-open:rotate-180">
          <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor"
            stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24">
            <path d="M6 9l6 6 6-6"></path>
          </svg>
        </span>
      `;

                const answerParagraph = document.createElement('p');
                answerParagraph.className = 'text-neutral-600 mt-3 p-2 group-open:animate-fadeIn';
                var ul = document.createElement('ul');
                response[value].forEach(function (senten, index) {
                    var li = document.createElement('li');
                    li.className='m-1'
                    console.log(senten);
                    li.textContent = senten;
                    ul.appendChild(li);
                });
                answerParagraph.appendChild(ul);

                details.appendChild(summary);
                details.appendChild(answerParagraph);
                faqItem.appendChild(details);
                dtcontainer.appendChild(faqItem);
                
            }
            var countele = document.getElementById('dkcount');
            countele.innerText = dcount;



        });
    });
});



// window.onload = function() {
//   scanLinks();
//   findHighestLink();
// };


window.addEventListener("DOMContentLoaded", () => {
    // document.getElementById('extractButton').addEventListener('click', function () {
    //   extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {

    //     extensionAPI.tabs.sendMessage(tabs[0].id, { action: "extractPrice" });
    //   });
    // });

    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        extensionAPI.tabs.sendMessage(tabs[0].id, { action: "calcDiff" });
    });

    // extensionAPI.runtime.onMessage.addListener(
    //   function (request, sender, sendResponse) {
    //     if (request.price) {
    //       if (request.price > 0 && request.price < 1000) {
    //         extensionAPI.storage.local.set('hiddencost',request.price.toString());
    //       }
    //       else if (request.price > 0) {
    //         var s = 'extpri'
    //       }
    //     }
    //   }
    // );
})
// Listen for messages from content script

// extensionAPI.storage.onChanged.addListener(function (changes, namespace) {

//     var ul = document.createElement('ul');

//     storageList.forEach(function (value, index) {
//       var li = document.createElement('li');
//       li.textContent = value;
//       ul.appendChild(li);
//     });
//     var divUrl = document.getElementById('darkwords');
//     divUrl.innerHTML = '';
//     divUrl.appendChild(ul);

// });

// extensionAPI.storage.onChanged.addListener(function (changes, namespace) {

//   extensionAPI.runtime.sendMessage({ action: 'getData' });

// });

// extensionAPI.runtime.onMessage.addListener(function(request, sender, sendResponse) {
//   if (request.action === 'updateUI') {

//     updateUI(request.data);
//   }
// });

// function updateUI(data) {

//   var ul = document.getElementById('dksentences');
//   var li = document.createElement('li');
//         li.textContent = data;
//         ul.appendChild(li);
// }


function scanLinks() {
    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        extensionAPI.tabs.sendMessage(tabs[0].id, { action: 'scanLinks' });

        // extensionAPI.storage.local.get('links', function (result) {
        //     var storedLinks = result.links || {};

        //     document.getElementById('result').innerHTML = JSON.stringify(storedLinks, null, 2);

        // });
    });
}

function findHighestLink() {
    extensionAPI.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        extensionAPI.tabs.sendMessage(tabs[0].id, { action: 'findHighestLink' });

    });
}


// function findHighestLink() {
//   extensionAPI.storage.local.get('links', function (result) {


//     let style = document.createElement('style');
//   style.textContent = `
//     a[data-highlighted="true"] {
//       background-color: yellow !important;
//       border: 2px solid red !important;
//     }
//   `;

//   document.head.appendChild(style);

//     const storedLinks = result.links || {};
//     let highestLink = null;
//     let highestValue = -1;

//     // Find the link with the highest value
//     for (const [link, value] of Object.entries(storedLinks)) {
//       if (value > highestValue) {
//         highestLink = link;
//         highestValue = value;
//       }
//     }

//     if (highestLink !== null) {
//       console.log('Link with the highest value:', highestLink, 'with value:', highestValue);
//       alert('Link with the highest value:\n' + highestLink + '\nwith value: ' + highestValue);
//     } else {
//       console.log('No links found in storage.');
//       alert('No links found in storage.');
//     }

//     let links = Array.from(document.links);
//     for (let i = 0; i < links.length; i++) {

//       if (links[i].href === highestLink) {
//         links[i].setAttribute('data-highlighted', 'true');
//         alert(1);
//       } else {
//         links[i].removeAttribute('data-highlighted');
//       }
//     }
//   });
// }

function clearStorage() {
    extensionAPI.storage.local.clear(function () {
        console.log('Storage cleared.');
        alert('Storage cleared.');
    });
}