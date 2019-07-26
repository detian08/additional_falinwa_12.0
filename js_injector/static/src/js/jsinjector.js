odoo.define('js_injector.jsinjector', function (require) {
  "use strict";
  var rpc = require('web.rpc');
  var core = require('web.core');
  var qweb = core.qweb;

  var debug = true;
  function log(msg){
    if(debug)
    {
      console.log('[jsinjector | 0.1]',msg);
    }
  }

  rpc.query({
    model: 'js.injector',
    method: 'get_current_user_static',
  })
  .then(function (result) {
    //log(result)

    if(!odoo['_xvi'])
      odoo['_xvi'] = {}
  
    odoo['_xvi']['js.injector'] = result;

    if(result.css && result.css.length > 5){
      var style = document.createElement('style');
      style.type = 'text/css';
      style.innerHTML = result.css
      log(`Add CSS`)
      document.getElementsByTagName('head')[0].appendChild(style);    
    };
    
    if(result.xml && result.xml.length > 0){
      log(`There is XML`);
      result.xml.map(x => {
        if(x)
        {
          log(`Load XML`)
          qweb.add_template(x);
        }
      })
    }

    if(result.js && result.js.length > 5){
      log(`Eval JS`)
      eval(result.js);
    }
  });
});