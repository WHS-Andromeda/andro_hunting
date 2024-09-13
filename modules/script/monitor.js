Java.perform(function() {
    console.log("[*] Starting Android monitoring script");

    // Deep Link Monitoring Section
    var Intent = Java.use("android.content.Intent");
    Intent.getData.implementation = function() {
        var action = this.getAction() !== null ? this.getAction().toString() : false;
        if (action) {
            console.log("[Deeplink] Intent.getData() was called");
            console.log("[Deeplink] Activity: " + this.getComponent().getClassName());
            console.log("[Deeplink] Action: " + action);
            var uri = this.getData();
            if (uri !== null) {
                // Logging URI information
                console.log("[Deeplink] Data:");
                uri.getScheme() && console.log("- Scheme: " + uri.getScheme() + "://");
                uri.getHost() && console.log("- Host: " + uri.getHost());
                uri.getPath() && console.log("- Path: " + uri.getPath());
                uri.getQuery() && console.log("- Params: " + uri.getQuery());
                uri.getFragment() && console.log("- Fragment: " + uri.getFragment());
            } else {
                console.log("[Deeplink] No data supplied.");
            }
        }
        return this.getData();
    };

    // WebView JavaScript Interface (JSI) Monitoring Section 
    var webView = Java.use('android.webkit.WebView');
    var webSettings = Java.use('android.webkit.WebSettings');
    var JavascriptInterface = Java.use('android.webkit.JavascriptInterface');

    var addedInterfaces = [];

    webSettings.setJavaScriptEnabled.implementation = function(allow) {
        console.log('[WebView] JavaScript Enabled: ' + allow);
        return this.setJavaScriptEnabled(allow);
    };

    // Monitor and hook JavaScript interface additions
    webView.addJavascriptInterface.implementation = function(object, name) {
        console.log('[JSI] JavaScript interface detected: ' + object.$className + ' instantiated as: ' + name);
        addedInterfaces.push(name);

        var interfaceClass = Java.use(object.$className);
        var methods = interfaceClass.class.getDeclaredMethods();
        methods.forEach(function(method) {
            var methodName = method.getName();
            if (method.isAnnotationPresent(JavascriptInterface.class)) {
                var overloads = interfaceClass[methodName].overloads;
                overloads.forEach(function(overload) {
                    overload.implementation = function() {
                        var args = [].slice.call(arguments);
                        console.log('[JSI] ' + name + '.' + methodName + ' called with args: ' + JSON.stringify(args));
                        var result = this[methodName].apply(this, arguments);
                        console.log('[JSI] ' + name + '.' + methodName + ' returned: ' + result);
                        return result;
                    };
                });
                console.log('[JSI] Hooked method: ' + name + '.' + methodName + ' (overloads: ' + overloads.length + ')');
            }
        });

        // Update JSI list in WebView 
        var updateScript = "window.frida_interfaces = " + JSON.stringify(addedInterfaces) + ";";
        this.evaluateJavascript(updateScript, null);

        return this.addJavascriptInterface(object, name);
    };

    // Monitor JavaScript evaluation
    webView.evaluateJavascript.implementation = function(script, resultCallback) {
        console.log('[WebView] evaluateJavascript called with script: ' + script);
        this.evaluateJavascript(script, Java.use("android.webkit.ValueCallback").$new({
            onReceiveValue: function(value) {
                console.log('[WebView] evaluateJavascript result: ' + value);
                if (resultCallback) {
                    resultCallback.onReceiveValue(value);
                }
            }
        }));
    };

    // Monitor JavaScript interface removal
    webView.removeJavascriptInterface.implementation = function(name) {
        console.log('[JSI] The ' + name + ' JavaScript interface removed');
        var index = addedInterfaces.indexOf(name);
        if (index > -1) {
            addedInterfaces.splice(index, 1);
            // Update interface list in WebView
            var updateScript = "window.frida_interfaces = " + JSON.stringify(addedInterfaces) + ";";
            this.evaluateJavascript(updateScript, null);
        }
        this.removeJavascriptInterface(name);
    };

    // Monitor URL loading and inject JavaScript for JSI call tracing
    webView.loadUrl.overload('java.lang.String').implementation = function(url) {
        console.log('[WebView] Loading URL: ' + url);
        this.loadUrl(url);

        // Inject JavaScript code for JSI call tracing 
        var js = `
            (function() {
                function wrapInterface(interfaceName) {
                    if (window[interfaceName]) {
                        for (var prop in window[interfaceName]) {
                            if (typeof window[interfaceName][prop] === 'function') {
                                var original = window[interfaceName][prop];
                                window[interfaceName][prop] = function() {
                                    console.log('JS called: ' + interfaceName + '.' + prop + ' with args: ' + JSON.stringify([].slice.call(arguments)));
                                    return original.apply(this, arguments);
                                };
                            }
                        }
                    }
                }

                // Initial wrapping
                var interfaces = window.frida_interfaces || [];
                interfaces.forEach(wrapInterface);

                // Set up observer to watch for changes to frida_interfaces
                var observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        if (mutation.type === 'childList') {
                            var newInterfaces = JSON.parse(mutation.target.textContent);
                            newInterfaces.forEach(wrapInterface);
                        }
                    });
                });

                var target = document.createElement('div');
                target.id = 'frida_interfaces_container';
                target.style.display = 'none';
                document.body.appendChild(target);

                observer.observe(target, { childList: true });

                Object.defineProperty(window, 'frida_interfaces', {
                    set: function(value) {
                        target.textContent = JSON.stringify(value);
                    },
                    get: function() {
                        return JSON.parse(target.textContent || '[]');
                    }
                });
            })();
        `;
        this.evaluateJavascript(js, null);
    };

    console.log("[*] Android monitoring script loaded successfully");
});