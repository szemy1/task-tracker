/****************************************************************************
**
** Copyright (C) 2014 Digia Plc and/or its subsidiary(-ies).
** Contact: http://www.qt.io/licensing/
**
** This file is part of the Qt WebChannel module.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and Digia. For licensing terms and
** conditions see http://qt.io/licensing. For further information
** use the contact form at http://qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

(function() {
    "use strict";

    function QWebChannel(transport, initCallback)
    {
        if (typeof transport !== "object" || typeof transport.send !== "function") {
            console.error("The QWebChannel expects a transport object with a send function and onmessage callback property." +
                          " Given is: transport: " + typeof(transport) + ", transport.send: " + typeof(transport.send));
            return;
        }

        var channel = this;
        this.transport = transport;

        this.send = function(data)
        {
            if (typeof data !== "string") {
                data = JSON.stringify(data);
            }
            channel.transport.send(data);
        };

        this.transport.onmessage = function(message)
        {
            var data = message.data;
            if (typeof data === "string") {
                data = JSON.parse(data);
            }
            switch (data.type) {
            case "signal":
                channel.objects[data.object].__qtSignals__[data.signal].apply(channel.objects[data.object], data.args);
                break;
            case "propertyUpdate":
                for (var i in data.data) {
                    var propertyData = data.data[i];
                    channel.objects[propertyData.object][propertyData.property] = propertyData.value;
                }
                break;
            case "init":
                channel.debug = data.debug;
                for (var objectName in data.objects) {
                    var object = new QObject(objectName, data.objects[objectName], channel);
                }
                if (initCallback) {
                    initCallback(channel);
                }
                channel.execCallbacks();
                break;
            default:
                console.error("invalid message received:", message.data);
                break;
            }
        };

        this.objects = {};

        this.execCallbacks = function()
        {
            for (var i = 0; i < this.execCallbacks.length; ++i) {
                this.execCallbacks[i]();
            }
            this.execCallbacks = [];
        };

        this.execCallbacks = [];
    }

    function QObject(name, data, webChannel)
    {
        this.__id__ = name;
        webChannel.objects[name] = this;

        for (var propertyIdx in data.properties) {
            var propertyData = data.properties[propertyIdx];
            var propertyName = propertyData.name;
            var propertyValue = propertyData.value;

            Object.defineProperty(this, propertyName, {
                configurable: true,
                get: function() {
                    return propertyValue;
                },
                set: function(value) {
                    if (value !== propertyValue) {
                        propertyValue = value;
                        webChannel.send({
                            type: "setProperty",
                            object: name,
                            property: propertyName,
                            value: value
                        });
                    }
                }
            });
        }

        this.__qtSignals__ = {};
        this.__qtCallbacks__ = {};

        for (var signalIdx in data.signals) {
            var signalData = data.signals[signalIdx];
            var signalName = signalData;

            this.__qtSignals__[signalName] = [];
            this[signalName] = (function(signalName) {
                return function() {
                    var args = Array.prototype.slice.call(arguments);
                    webChannel.send({
                        type: "signal",
                        object: name,
                        signal: signalName,
                        args: args
                    });
                };
            })(signalName);
        }

        for (var methodIdx in data.methods) {
            var methodData = data.methods[methodIdx];
            var methodName = methodData;

            this[methodName] = (function(methodName) {
                return function() {
                    var args = Array.prototype.slice.call(arguments);
                    var callback;
                    if (args.length > 0 && typeof args[args.length - 1] === "function") {
                        callback = args.pop();
                    }
                    webChannel.execCallbacks.push(callback);
                    webChannel.send({
                        type: "invokeMethod",
                        object: name,
                        method: methodName,
                        args: args
                    });
                };
            })(methodName);
        }
    }

    window.QWebChannel = QWebChannel;
})();