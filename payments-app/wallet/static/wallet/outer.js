(function(window) {
  var document = window.document;

  function receiveMessage(event) {
    if (event.origin !== "http://localhost:8000") return;
    console.log('reveived', event);
  }

  function appendIframe() {
    var iframe = document.createElement('iframe');
    iframe.style.display = "none";
    iframe.src = "http://localhost:8000/iframe";
    document.body.appendChild(iframe);
  }



  window.addEventListener("message", receiveMessage, false);

})();