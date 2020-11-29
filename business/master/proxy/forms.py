import pickle
import datetime

from wtforms import StringField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import ValidationError

from pickle_data.pickles import pick_proxy
from common.form import IVsForm


class ProxyAddForm(FlaskForm):
    # 代理
    proxy = StringField('proxy',
                        [validators.required(message="代理必填")])

    @staticmethod
    def validate_proxy(_, field):

        proxy = field.data
        proxy = proxy.replace(' ', '').replace('，', ';').replace('\r', '').replace('\n', '')
        proxy_list = proxy.split(';')
        proxy_list = [p for p in proxy_list if p]
        f = filter(lambda x: ':' not in x, proxy_list)
        errors = []
        for e in f:
            errors.append(e)

        def valid_address(item):
            ip, port = item.split(':')
            if not port.isdigit():
                errors.append(item)
            else:
                if int(port) > 65535 or int(port) < 1:
                    errors.append(item)
                else:
                    if '.' not in ip:
                        errors.append(item)
                    else:
                        ip = ip.split('.')
                        for i in ip:
                            if not i.isdigit():
                                errors.append(item)
                                continue
                            if int(i) > 255 or int(i) < 0:
                                errors.append(item)
                                continue
                            if i.startswith('0') and i != '0':
                                errors.append(item)
                                continue

        f = map(valid_address, proxy_list)
        for _ in f:
            pass

        if errors:
            raise ValidationError('代理格式错误: %s' % ', '.join(errors))

    def data_parser(self):
        proxy = self.proxy.data
        proxy = proxy.replace(' ', '').replace('，', ';').replace('\r', '').replace('\n', '')
        proxy_list = proxy.split(';')
        proxy_list = [p for p in proxy_list if p]

        with open(pick_proxy, 'rb') as f:
            proxy = pickle.load(f)
            proxy_list = [p for p in proxy_list if p not in proxy]

        time = str(datetime.datetime.now())
        proxy_dict = dict([(p, {'proxy': p, 'add_time': time,
                                'version': 1,
                                'status': '未知', 'business': []}) for p in proxy_list])
        return proxy_dict


class ProxyDeleteForm(IVsForm):

    def validate_ids(self, _):
        pass
