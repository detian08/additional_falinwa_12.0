class fal_rainloop_integration {
    constructor(opts) {
        const s = this;
        s.debug = opts.debug || false;
        s.$ = opts.$;
        s.odoo = opts.odoo;
        s.session = opts.session;
        s.version = opts.version || "0.0";
    }

    log(msg) {
        const s = this;
        if (s.debug) {
            console.log(msg);
        }
    }

    start() {
        const s = this;
        s.log(`start: ${s.version}`);
        s.buildSystray();
        s.setEvents();
    }

    buildSystray() {
        const s = this;
        s.log(`buildSystray`);
        //Appends Icon template in system tray(navbar)
        var IconMenu = s.odoo.Widget.extend({
            template: 'fal_rainloop_systray_integration',
        });
        s.odoo.SystrayMenu.Items.push(IconMenu);
    }

    setEvents() {
        const s = this;
        s.log(`setEvents`);
        // console.log(s.$('a.fal_rainloop_btn'));

        var myLoop = setInterval(function () {
            if (s.$('a.fal_rainloop_btn').length > 0) {
                s.$('a.fal_rainloop_btn').click(function (e) {
                    e.preventDefault();
                    s.$(this).parent().toggleClass('show');
                    s.toggleMailbox();
                });
                clearInterval(myLoop);
            }
        }, 250)
    }

    buildIframe(url) {
        const s = this;
        s.log(`buildIframe: ${url}`);
        var style = [
            'background-color:#ccc',
            'width:100%',
            'position:absolute',
            'z-index:1000',
            `top: ${s.$('header').height()}px`,
            `height: ${s.$(window).height() - s.$('header').height()}px`
        ];
        style = style.join(';');
        var obj = '<iframe class="fal_rainloop_iframe" style="' + style + '" src="' + url + '" />';
        s.$(obj).appendTo('body');
    }

    async getUserInfo() {
        const s = this;
        s.log(`getUserInfo`);
        if (s.user) {
            return s.user;
        }
        var query = {
            model: 'res.users',
            method: 'search_read',
            args: [
                [['id', '=', s.session.uid]],
                [
                    "id",
                    "login",
                     "x_studio_email_pass",
                     "x_studio_webmail_sso_key",
                     "x_studio_webmail_domain"
                ],
                0,
                1,
                false
            ]
        };
        s.user = await s.odoo.RPC.query(query);
        if(s.user.length > 0){
            s.user = s.user[0];
        }
        return s.user;
    }

    async getAutoLoginUrl() {
        const s = this;
        s.log(`getAutoLoginUrl`);

        await s.getUserInfo();

        if (!s.user) {
            throw new Error("No user info");
        }

        //{"content-type": "application/x-www-form-urlencoded"}
        var token = await s.$.post(
            'https://' + s.user.x_studio_webmail_domain + '/index.php?ExternalSso',
            {
                'SsoKey': s.user.x_studio_webmail_sso_key,
                'Email': s.user.login,
                'Password': s.user.x_studio_email_pass
            })
        return 'https://' + s.user.x_studio_webmail_domain + '?sso&hash=' + token;
    }

    toggleMailbox() {
        const s = this;
        s.log(`toggleMailbox`);

        var iframe = s.$('.fal_rainloop_iframe');
        if (iframe.length === 0) {
            s.getAutoLoginUrl()
                .then(url => {
                    console.log(url)
                    s.buildIframe(url);
                    iframe = s.$('.fal_rainloop_iframe');
                    iframe.show();
                }).catch(e => {
                    s.log(`Error when generating auto login url !`)
                    console.error(e);
                });
            return true;
        } else {
            if (iframe.is(':visible')) {
                iframe.hide();
            } else {
                iframe.show();
            }
        }
    }

}

odoo.define('fal_rainloop_integration', function (require) {
    "use strict";
    var lib = {
        RPC: require('web.rpc'),
        SystrayMenu: require('web.SystrayMenu'),
        Widget: require('web.Widget')
    };
    $(function () {
        let instance = new fal_rainloop_integration({
            version: "0.004",
            debug: true,
            $: $,
            odoo: lib,
            session: odoo.session_info
        });
        instance.start();
        return instance;
    });
});