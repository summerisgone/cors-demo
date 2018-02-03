(function() {

  var PAYMENT_ORIGIN = 'https://payments.summerisgone.com';
  var TX_URL = `${PAYMENT_ORIGIN}/api/tx`;
  var WALLET_URL = `${PAYMENT_ORIGIN}/api/wallet/`;
  var LOGIN_URL = `${PAYMENT_ORIGIN}/accounts/login/`;
  var TOKEN_URL = `${PAYMENT_ORIGIN}/token`;


  function getToken() {
    return new Promise((resolve, reject) => {
      var iframe = document.createElement('iframe');
      var retry = 0;
      var tokenReady = false;
      iframe.src = TOKEN_URL;
      iframe.width = 0;
      iframe.height = 0;
      iframe.style.opacity = 0;
      document.body.appendChild(iframe);
      iframe.onload = () => {
        function _getToken() {
          if (tokenReady) return;
          iframe.contentWindow.postMessage('getToken', PAYMENT_ORIGIN);
          retry++;
          if (retry < 3) {
            setTimeout(_getToken, 500);
          } else {
            console.error('unauthorised');
            reject('unauthorised');
          }
        }
        _getToken();
      }

      function receiveMessage(event)
      {
        if (event.data.startsWith && event.data.startsWith('token')) {
          console.log('token is', event.data);
          resolve(event.data.split(':')[1]);
          tokenReady = true;
        }
      }
    
      window.addEventListener('message', receiveMessage, false);
    });
  }

  function openAuth(resolve, reject) {
    var authWindow = window.open(LOGIN_URL, "hello", "width=200,height=200,left=500,top=300");
    function receiveMessage(event) {
      if ((event.origin === PAYMENT_ORIGIN) &&
        (event.data === 'close')) {
          authWindow.close();
          resolve();
        }
    }
    window.addEventListener('message', receiveMessage, false);
    // close popup after 10s
    setTimeout(() => {
      reject('unauthorized')
    }, 10000);
  }

  function getBalance(token) {
    return fetch(WALLET_URL, {
      method: 'GET',
      mode: 'cors',
      credentials: 'include',
      headers: new Headers({
        'Authorization': `Token ${token}`
      })
    }).then(response => response.json());
  }

  function sendMoney(token, options) {
    return fetch(TX_URL, {
      method: 'POST',
      mode: 'cors',
      credentials: 'include',
      headers: new Headers({
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify(options)
    })
  }

  window.SDK = {
    openAuth,
    getToken,
    getBalance,
    sendMoney
  }
  
})();