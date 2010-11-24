<%
from mako.template import Template
import os
import os.path
from os.path import join as opjoin
import racy.rutils as rutils

NAMESPACE = []
path = opjoin('include', PRJ_NAME)
temp_file = TEMP_DIR + '/' + 'namespace_dir.hpp'


for i in SRV_SPLITTED_PATH:
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

namespace ${i}
{

} // namespace ${i}








