let ModelLP = {
    'model': {
        'id': 'arrowMapSettingModal',
        'url': '',
    },
    'show': function () {
        $("#" + this.model.id).modal('show');
    },
    'hide': function () {
        $("#" + this.model.id).modal('hide');
    },
    'fresh': function (data) {
        let i;
        let field;
        let fields = $("#" + this.model.id + ' .f-data');

        console.log('fresh', data);
        for (i = 0; i < fields.length; i++) {
            field = fields[i];
            if (field.name === undefined) {
                continue
            }

            if (data[field.name] === undefined) {
                continue
            }
            console.log(field.name);
            this.fill_one(field, data[field.name]);
        }
    },
    'fill_one': function (field, value) {
        let local_name = field.localName;
        if (local_name === 'input') {
            $(field).val(value);
        } else if (local_name === 'span') {
            $(field)[0].textContent = value;
        } else if (local_name === 'select') {
            $(field).each(function () {
                let that = this;
                if ($(that).hasClass('selectpicker')) {
                    // bootstrap-select
                    $(that).selectpicker('val', value)
                } else {
                    // normal select
                    alert('normal select. ');
                }
            });
        } else if (local_name === 'textarea') {
            $(field).val(value);
        }
    },
    'request': function (params) {
        let that = this;
        if (params.data === undefined) {
            params.data = $("#" + this.model.id + ' form').serialize();
        }

        if (params.url === undefined) {
            params.url = this.model.url;
        }

        if (params.after !== undefined) {
            let f = params.after;
            // 已定义成功回调
            // 添加模态框收起
            function ffff(rsp, p) {
                if (that.model.id !== '') {
                    $('#' + that.model.id).modal('hide');
                    let table = $('#' + that.model.id + ' table');
                    if (table.length > 0) {
                        table.bootstrapTable('refresh');
                    }
                }
                f(rsp, p);
            }

            params.after = ffff;
        } else {
            let f = params.success;

            if (params.success === undefined) {
                // 未定义成功回调
                function ff() {
                    $('#' + that.model.id).modal('hide');
                    let table = $('#' + that.model.id + ' table');
                    if (table.length > 0) {
                        table[0].bootstrapTable('refresh');
                    }
                }

                params.success = ff;
            } else {
                // 已定义成功回调
                // 添加模态框收起
                function fff(rsp, p) {
                    if (that.model.id !== '') {
                        $('#' + that.model.id).modal('hide');
                        let table = $('#' + that.model.id + ' table');
                        if (table.length > 0) {
                            table.bootstrapTable('refresh');
                        }
                    }
                    f(rsp, p);
                }

                params.success = fff;
            }
        }

        console.log('post', params);
        if (params.m === 'post') {
            post(params);
        } else {
            get(params)
        }
    },
    'get': function (params) {
        params.m = 'get';
        this.request(params)
    },
    'post': function (params) {
        params.m = 'post';
        this.request(params)
    },
    'json': function () {
        let json = {};
        let fields = $("#" + this.model.id + ' .f-data');
        let i, field, name;

        for (i = 0; i < fields.length; i++) {
            field = fields[i];
            name = field.name;

            let local_name = field.localName;
            let value;
            if (local_name === 'input') {
                value = $(field).val();
            } else if (local_name === 'span') {
                value = $(field)[0].textContent;
            } else if (local_name === 'select') {
                $(field).each(function () {
                    let that = this;
                    if ($(that).hasClass('selectpicker')) {
                        // todo: 可能会有问题
                        value = $(that).selectpicker('val');
                    } else {
                        // normal select
                        alert('normal select. ');
                    }
                });
            } else if (local_name === 'textarea') {
                value = $(field).val();
            }
            if (json[name] === undefined) {
                json[name] = value;
            } else {
                if (json[name] instanceof Array) {
                    json[name].push(value);
                } else {
                    let tmp = json[name];
                    json[name] = [tmp, value]
                }
            }
        }
        console.log('json', json);
        return json;
    }
};

// 登录模型
let login_model = {
    // {# 模型id#}
    'id': 'login-model',
    // {# 路由#}
    'url': '/user/login'
};

let Login = Object.create(ModelLP);
Login.model = login_model;


// 注册模型
let register_model = {
    'id': 'register-model',
    'url': '/user/register'
};

let Register = Object.create(ModelLP);
Register.model = register_model;


// 更新密钥模型
let update_cipher_model = {
    'id': '',
    'url': '/cipher/update'
};

let UpdateCipher = Object.create(ModelLP);
UpdateCipher.model = update_cipher_model;


// 添加代理模型
let add_proxy_model = {
    'id': 'proxy-add-modal',
    'url': '/proxy/add'
};

let AddProxy = Object.create(ModelLP);
AddProxy.model = add_proxy_model;


// 删除代理模型
let delete_proxy_model = {
    'id': '',
    'url': '/proxy/delete'
};

let DeleteProxy = Object.create(ModelLP);
DeleteProxy.model = delete_proxy_model;


// 编辑节点模型
let edit_node_model = {
    'id': 'node-edit-modal',
    'url': '/node/edit'
};

let EditNode = Object.create(ModelLP);
EditNode.model = edit_node_model;


// 检测节点模型
let check_node_model = {
    'id': '',
    'url': '/node/check'
};

let NodeCheck = Object.create(ModelLP);
NodeCheck.model = check_node_model;

// 添加主控模型
let add_master_model = {
    'id': 'master-add-modal',
    'url': '/master/add'
};

let MasterAdd = Object.create(ModelLP);
MasterAdd.model = add_master_model;


// 添加任务模型
let add_task_model = {
    'id': 'task-add-modal',
    'url': '/task/add'
};

let TaskAdd = Object.create(ModelLP);
TaskAdd.model = add_task_model;

// 编辑任务模型
let edit_task_model = {
    'id': 'task-edit-modal',
    'url': '/task/edit'
};

let TaskEdit = Object.create(ModelLP);
TaskEdit.model = edit_task_model;


// 删除任务模型
let delete_task_model = {
    'id': '',
    'url': '/task/delete'
};

let TaskDelete = Object.create(ModelLP);
TaskDelete.model = delete_task_model;

// 运行任务模型
let run_task_model = {
    'id': 'task-run-modal',
    'url': '/task/run'
};

let TaskRun = Object.create(ModelLP);
TaskRun.model = run_task_model;
