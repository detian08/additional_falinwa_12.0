class fal_iframe_integration_js {
  constructor({
    debug = true,
    version = "0.1",
    $ = false,
    lib = false
  }) {
    const s = this;
    s.debug = false;
    s.$ = $;
    s.lib = lib;
    s.version = version || "0.0";
    s.className = s.constructor.name;
    s.session = odoo.session_info || false;
    //console.log(s.session)
  }

  log(msg) {
    const s = this;
    if (s.debug) {
      console.log(`${s.className} | ${s.version}`, msg);
    }
  }

  start() {
    const s = this;
    s.log(`start: ${s.version}`);
    try {
      s.asyncStart();
    } catch (e) {
      console.error(e);
    }
  }

  async getUserInfo() {
    const s = this;
    s.log(`getUserInfo`);
    var limit = 10;

    var query = {
      model: 'res.users',
      method: 'search_read',
      args: [
        [['id', '=', s.session.uid]],
        ['id', 'name', 'groups_id'],
        0,
        limit,
        false
      ]
    };
    return await s.lib.RPC.query(query);
  }


  async getIframeIntegrations() {
    const s = this;
    s.log(`getIframeIntegrations`);
    var limit = 10;

    var query = {
      model: 'fal.iframe_integration',
      method: 'search_read',
      args: [
        [['active', '=', true], ['groups', '=', s.userInfo.groups_id]],
        [],
        0,
        limit,
        false
      ]
    };
    //console.log(query)
    return await s.lib.RPC.query(query);
  }

  async asyncStart() {
    const s = this;
    s.log(`asyncStart`);

    // fal_iframe_integration
    //  s.lib.qweb.add_template('fal_iframe_integration/static/src/xml/fal_iframe_integration.xml');

    s.userInfo = await s.getUserInfo();
    if (s.userInfo.length > 0) {
      s.userInfo = s.userInfo[0];
    } else {
      return false;
    }
    //console.log(s.userInfo);

    s.integrations = await s.getIframeIntegrations();
    //console.log(s.integrations)

    if (s.integrations.length === 0) {
      s.log(`No integrations, skip.`);
      return false;
    }

    s.$(window).resize(function () {
      s.$('iframe.fal_iframe_integration').each(function (index) {
        var iframeSelector = 'iframe#' + s.$(this).attr('id');
        s.resizeIframe(iframeSelector);
      });
    });

    var now = new Date().getTime();
    s.integrations.map(i => {
      s.buildSystray({
        id: (now).toString(),
        title: i.title,
        iframeUrl: i.url,
        iconClass: i.icon || "plus",
      });
      now = now + 1;
    })
  }

  buildSystray({
    id = false,
    title = false,
    iframeUrl = false,
    iconClass = 'plus'
  }) {
    const s = this;
    s.log(`buildSystray`);
    if (!title || !iframeUrl || !id) {
      s.log('iframe not configured properly')
      return false;
    }

    //  console.log('test')
    var IconMenu = s.lib.Widget.extend({
      template: 'fal_iframe_integration_views_systray',
      init: function (parent) {
        this._super(parent);
        this.title = title;
        this.iframeUrl = iframeUrl;
        this.id = id;
        this.iframeId = `iframe-${id}`;
        this.btnId = `btn-${id}`;
        this.iconClass = "fa fa-" + iconClass;
      },
      events: {
        'click .fal_iframe_integration_btn': function (e) {
          e.preventDefault();
          var self = this;

          var btnSelector = '#' + self.btnId;
          var iframeSelector = '#' + self.iframeId;
          var btn = self.$(btnSelector);
          var iframe = s.$(iframeSelector);

          //  console.log(btn)
          //console.log(btn.parent())
          //  console.log(iframe)

          btn.parent().toggleClass('show');

          if (iframe.length === 0) {
            s.buildIframe(self.iframeId, self.iframeUrl);
            s.resizeIframe(iframeSelector);
            iframe = s.$(iframeSelector);
            iframe.show();
            return true;
          } else {
            if (iframe.is(':visible')) {
              iframe.hide();
            } else {
              iframe.show();
            }
          }
        }
      },
      start: function () {
        s.log('Starting for iframe ' + this.title);
      },
    });
    s.lib.SystrayMenu.Items.push(IconMenu);
  }

  buildIframe(id, url) {
    const s = this;
    s.log(`buildIframe: ${url}`);
    var obj = `<iframe id="${id}" class="fal_iframe_integration" src="${url}" />`;
    s.$(obj).appendTo('body');
  }

  resizeIframe(iframeSelector) {
    const s = this;
    s.log(`resizeIframe: ${iframeSelector}`);
    var iframe = s.$(iframeSelector);
    if (iframe.length > 0) {
      s.$(iframeSelector).css('top', `${s.$('header').height()}px`);
      s.$(iframeSelector).css('height', `${s.$(window).height() - s.$('header').height()}px`);
    }
  }

}

odoo.define('fal_iframe_integration_js', function (require) {
  "use strict";
  var lib = {
    RPC: require('web.rpc'),
    Core: require('web.core'),
    SystrayMenu: require('web.SystrayMenu'),
    Widget: require('web.Widget')
  };
  $(function () {
    lib['qweb'] = lib.Core.qweb;
    let instance = new fal_iframe_integration_js({
      version: "0.007",
      debug: true,
      $: $,
      lib: lib
    });
    instance.start();
    return instance;
  });
});