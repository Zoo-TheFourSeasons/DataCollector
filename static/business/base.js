

axios.interceptors.response.use(function (response) {
    // hook response
    let content = "";
    let message = response.data.messages;

    if (message === undefined) {
        return response;
    }
    if (typeof message === 'object' && Object.keys(message).length !== 0) {
        content = Object.values(message).join('<br>');
    }
    else if (typeof message === 'string') {
        content = message;
    }

    if (response.data.status) {
        // 执行成功
        // 仍然有消息要显示
        if (content) {

        }
    }
    else {
        // 执行失败
        // confirm 强制显示
        if (content) {
            confirm_tip('警告! ', content)
        }
    }
    return response;
});


function confirm_tip(title, content) {
    // 提示信息
    let confirm = $.confirm({
        closeIcon: false,
        columnClass: 'col-md-12',
        theme: 'supervan',
        type: 'red',
        title: title,
        content: content,
        buttons: {
            cancel: {
                text: '关闭',
                btnClass: 'btn-warning'
            }
        }
    });
    confirm.open();
}


function request(params) {
    let url = params.url;
    let method = params.method;
    let data = params.data;
    let success = params.success;
    let success_params = params.success_params;
    let failed = params.failed;
    let failed_params = params.failed_params;
    let btn = params.btn;
    let header = params.header;
    let after = params.after;
    let after_params = params.after_params;

    if (header === undefined){
        header = {}
    }

    let config;
    if (method === "get") {
        config = {url: url, method: method, params: data, headers: header}
    }
    else if (method === 'post') {
        config = {url: url, method: method, data: data, headers: header}
    }

    if (btn !== undefined) {
        btn.attr('disabled', 'true');
    }
    axios.request(config)
        .then(function (response) {
            // 结束回调
            if (after !== undefined) {
                after(response, after_params)
            }
            else {
                // 正常回调
                if (response.data.status) {
                    if (success !== undefined) {
                        success(response, success_params);
                    }
                }
                // 错误回调
                else {
                    if (failed !== undefined) {
                        failed(response, failed_params);
                    }
                }
            }
            if (btn !== undefined) {
                btn.attr('disabled', false);
            }
        })
        .catch(function (error) {
            if (btn !== undefined) {
                btn.attr('disabled', false);
            }
            console.log(error);
        });
}


function post(params) {
    params.method = 'post';
    request(params)
}


function get(params) {
    params.method = 'get';
    request(params)
}


// 获取表格 id 字段
function get_table_id_field(table) {
    let id_field = '';
    for (let i =0; i<table.length; i++) {
        if (Object.keys(table[i].dataset).length === 0) {
            break
        }
        if (Object.keys(table[i].dataset.idField).length === 0) {
            break
        }
        id_field = table[i].dataset['idField'];
    }
    return id_field
}

// 获取表格已选数据 id
function get_table_selected_id(table, id_field) {
    let data = table.bootstrapTable('getSelections');
    let ids = [];
    for (let k = 0; k < data.length; k++) {
        ids.push(data[k][id_field])
    }
    return ids
}


function buildTable($el, cells, rows) {
    let i;
    let j;
    let row;
    let columns = [];
    let data = [];

    for (i = 0; i < cells; i++) {
        columns.push({
            field: 'field' + i,
            title: 'Cell' + i,
            sortable: true
        })
    }
    for (i = 0; i < rows; i++) {
        row = {};
        for (j = 0; j < cells; j++) {
            row['field' + j] = 'Row-' + i + '-' + j
        }
        data.push(row)
    }

    $el.bootstrapTable('destroy').bootstrapTable({
        columns: columns,
        data: data,
        search: false,
        stickyHeader: true,
        theadClasses: 'thead-dark'
    })
}


//  模态框拖动 居中
$(document).on("show.bs.modal", ".modal", function () {
    $(this).draggable({cursor: 'move'});
    $(this).css("overflow", "hidden");
    $(this).css('display', 'block');
});


function get_selected($table, with_version) {
    let data = $table.bootstrapTable('getSelections');
    let ids_ = [];
    let versions_ = [];
    if (data.length === 0) {
        return {}
    }
    for (let i = 0; i < data.length; i++) {
        ids_.push(data[i].id);
        if (with_version) {
            versions_.push(data[i].version);
        }
    }
    if (with_version) {
        return {'ids': ids_.join(','), 'versions': versions_.join(',')};
    }
    return {'ids': ids_.join(',')};

}


function adjust_height(table) {
    let height = $(document).height() - table.offset().top;
    console.log('document', $(document).height());
    console.log(table.offset().top);
    table.bootstrapTable('resetView', {height: height});
    table.bootstrapTable('refresh');
}


function search_move(table) {
    let $search = $("#search");
    let $input = $(".search input");
    $search.empty();
    $search.append($(".fixed-table-toolbar"));

    $(".search").css("width", '100%');

    $input.addClass('form-control-dark w-100');
    $input.css("width", '100%');
    $input.attr('placeholder', '搜索');

    if (table === undefined)
        return ;
    adjust_height(table);
}


function k_(data, div_container) {
    console.log(div_container);
    console.log(data['hist']);
    console.log(data.start, data.end);

    var ds = new DataSet({
            state: {
                start: data.start,
                end: data.end
            }
        }
    );
    var dv = ds.createView();
    dv.source(data['hist']).transform({
        type: 'filter',
        callback: function callback(obj) {
            var date = obj.time;
            return date <= ds.state.end && date >= ds.state.start;
        }
    }).transform({
        type: 'map',
        callback: function callback(obj) {
            obj.trend = obj.start <= obj.end ? '上涨' : '下跌';
            obj.range = [obj.start, obj.end, obj.highest, obj.lowest];
            return obj;
        }
    });
    var chart = new G2.Chart({
        container: div_container,
        forceFit: true,
        height: 430,
        animate: true,
        padding: [10, 40, 40, 40]
    });
    chart.source(dv, {
        'time': {
            type: 'timeCat',
            nice: false,
            range: [0, 1]
        },
        trend: {
            values: ['上涨', '下跌']
        },
        'volume': {
            alias: '成交量'
        },
        'start': {
            alias: '开盘价'
        },
        'end': {
            alias: '收盘价'
        },
        'highest': {
            alias: '最高价'
        },
        'lowest': {
            alias: '最低价'
        },
        'range': {
            alias: '价格'
        }
    });
    chart.legend({
        offset: 20
    });
    chart.tooltip({
        showTitle: false,
        itemTpl: '<li data-index={index}>' + '<span style="background-color:{color};" class="g2-tooltip-marker"></span>' + '{name}{value}</li>'
    });

    var kView = chart.view({
        end: {
            x: 1,
            y: 0.5
        }
    });
    kView.source(dv);
    kView.schema().position('time*range').color('trend', function (val) {
        if (val === '上涨') {
            return '#f04864';
        }

        if (val === '下跌') {
            return '#2fc25b';
        }
    }).shape('candle').tooltip('time*start*end*highest*lowest', function (time, start, end, highest, lowest) {
        return {
            name: time,
            value: '<br><span style="padding-left: 16px">开盘价：' + start + '</span><br/>' + '<span style="padding-left: 16px">收盘价：' + end + '</span><br/>' + '<span style="padding-left: 16px">最高价：' + highest + '</span><br/>' + '<span style="padding-left: 16px">最低价：' + lowest + '</span>'
        };
    });

    var barView = chart.view({
        start: {
            x: 0,
            y: 0.65
        }
    });
    barView.source(dv, {
        volume: {
            tickCount: 2
        }
    });
    barView.axis('time', {
        tickLine: null,
        label: null
    });
    barView.axis('volume', {
        label: {
            formatter: function formatter(val) {
                return parseInt(val / 1000, 10) + 'k';
            }
        }
    });
    barView.interval().position('time*volume').color('trend', function (val) {
        if (val === '上涨') {
            return '#f04864';
        }

        if (val === '下跌') {
            return '#2fc25b';
        }
    }).tooltip('time*volume', function (time, volume) {
        return {
            name: time,
            value: '<br/><span style="padding-left: 16px">成交量：' + volume + '</span><br/>'
        };
    });

    // chart.interact('slider' + 'hist_1h', {
    //     container: 'slider' + 'hist_1h', // DOM id
    //     start: ds.state.start, // 和状态量对应
    //     end: ds.state.end,
    //     data: data['hist'], // 源数据
    //     xAxis: 'time', // 背景图的横轴对应字段，同时为数据筛选的字段
    //     yAxis: 'volume', // 背景图的纵轴对应字段，同时为数据筛选的字段
    //     scales: {
    //         time: {
    //             type: 'timeCat',
    //             nice: false
    //         }
    //     },
    //     onChange: function onChange(_ref) {
    //         var startText = _ref.startText,
    //             endText = _ref.endText;
    //
    //         ds.setState('start', startText);
    //         ds.setState('end', endText);
    //         setTimeout(function () {
    //             chart.render();
    //         }, 32);
    //     }
    // });
    chart.render();
}
