$(document).ready(function () {

    var search = $("#search");
    search.empty();
    search.append($(".fixed-table-toolbar"));
    $(".search").css("width", '100%');

    var search_input = $(".search input");
    search_input.addClass('form-control-dark w-100');
    search_input.css("width", '100%');


    var _DataSet = DataSet;
    var DataView = _DataSet.DataView;

    axios.request({url: '/hist/index', method: 'get', params: request.data})
        .then(function (response) {
            var dv = new DataView();
            dv.source(response.data.hists).transform({
                type: 'map',
                callback: function callback(obj) {
                    obj.stockRange = [obj.start, obj.end, obj.highest, obj.lowest];
                    return obj;
                }
            });
            var chart = new G2.Chart({
                container: 'mountNode',
                forceFit: true,
                height: window.innerHeight,
                animate: false
            });
            chart.source(dv, {
                'date': {
                    type: 'time',
                    nice: false,
                    mask: 'MM-DD',
                    tickCount: 10
                },

                'stockRange': {
                    min: 4,
                    max: 7,
                    nice: false
                }
            });
            chart.axis('mean', false);
            chart.axis('stockRange', false);
            chart.tooltip({
                crosshairs: {
                    type: 'line'
                }
            });
            chart.area().position('date*range').color('#64b5f6');
            chart.schema().position('date*stockRange').color('trend', function (val) {
                if (val === 'up') {
                    return '#f04864';
                }

                if (val === 'down') {
                    return '#2fc25b';
                }
            }).shape('candle').tooltip('start*end*highest*lowest');
            chart.line().position('date*mean').color('#FACC14');
            chart.render();
        })
        .catch(function (error) {
            console.log(error);
            catch_error(error);
        });
});