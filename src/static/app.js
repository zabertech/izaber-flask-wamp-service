// D3 graphics engine for data
// https://d3js.org
window.d3 = require('d3');

// Graphing library that relies on D3
// http://nvd3.org/
window.nvd3 = require('nvd3');

// Does this need introduction? No? Good.
window.jQuery = require('jquery');
window.$ = require('jquery');

// Lovely little animation library
// http://animejs.com/
window.anime = require('animejs');

// Great JS spreadsheet
// https://handsontable.com/
window.Handsontable = require('handsontable');
import 'handsontable.css';

// Create CSV files
// https://github.com/Inist-CNRS/node-csv-string
import * as CSV from 'csv-string';
window.CSV = CSV;

// Magic download buttons
// https://github.com/rndme/download
window.download = require('downloadjs');

// Support for jinja2 style templates
// https://mozilla.github.io/nunjucks/
window.nunjucks = require('nunjucks');

// Another template engine. Good, fast, infuriatingly purist about logic in templates
window.Handlebars = require("handlebars");

// Promise based HTTP client for the browser and node.js
// https://github.com/axios/axios
window.axios = require('axios');

// Support for Semantic UI
window.semantic = require('semantic-ui-offline');

// Autobahn WAMP support
window.autobahn = require('autobahn');

// FullCalendar: Really nice calendar support
// https://fullcalendar.io/
import 'fullcalendar';

// Font awesome support

// Terminal emulator widget!
// https://xtermjs.org/docs/guides/import/
import { Terminal } from 'xterm';
window.fit = require("xterm/lib/addons/fit/fit");
window.Terminal = Terminal;
Terminal.applyAddon(window.fit);

// Split.js - < 2kb unopinionated utility for resizeable split views.
// https://github.com/nathancahill/Split.js
window.Split = require('split.js');

// Ace Editor
window.Ace = require('ace-builds/src-noconflict/ace');
window.modelist = require('ace-builds/src-noconflict/ext-modelist.js');

// Cookie handling
// https://github.com/js-cookie/js-cookie
window.Cookies = require('js-cookie');

// jsTree. For tree viewing of files
// https://www.jstree.com/
window.jstree = require('jstree');
import 'jstree.css';
import 'jstree-dark.css';
//import('jstree');

// riot-route: Simple JS router
// https://github.com/riot/route/tree/master/doc
window.route = require('riot-route');

require('./js/main.js');
require('./css/main.css');

