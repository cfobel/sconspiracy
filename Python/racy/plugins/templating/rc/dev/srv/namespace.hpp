<%
from mako.template import Template
import os
import os.path
from os.path import join as opjoin
import racy.rutils as rutils

NAMESPACE = [PRJ_NAME]
path = opjoin('include', PRJ_NAME)
temp_file = TPL_DIR + '/' + 'namespace_dir.hpp'


for i in SRV_SPLITTED_PATH:
    print i
    path = opjoin(path, i)
    NAMESPACE.append(i)

    dict = {
        'NAMESPACE': NAMESPACE,
    }

    temp = Template(filename = temp_file)
    res = temp.render(**dict)

    rutils.put_file_content(path + '/namespace.hpp' , res)



%>


/**
*
*     TODO Doxygen documentation
*
**/

%for i in NAMESPACE:
namespace ${i}
{

%endfor
%for i in reversed(NAMESPACE):
} // namespace ${i}
%endfor






