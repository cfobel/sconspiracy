<% 
import os
import os.path
import sys



PATH = SRV_SPLITTED_PATH

COMPLETE_NAMESPACE = '::' + '::'.join(PATH) + '::' + SRV_NAME 

NAMESPACE = SRV_PATH.split('/')

NAMESPACE = [PRJ_NAME]
NAMESPACE.extend(PATH)


%>

#include "${SRV_PATH[1:]}/${SRV_NAME}.hpp"

REGISTER_SERVICE( /* SrvSuperClass */ , ${COMPLETE_NAMESPACE}  , /* Object */ ) ;


%for i in NAMESPACE:
namespace ${i}
{

%endfor

${SRV_NAME}::${SRV_NAME}()
{

}
                                                        
                                                        
void ${SRV_NAME}::starting() throw ( ::fwTools::Failed )
{

}

void ${SRV_NAME}::stopping() throw ( ::fwTools::Failed ) 
{

}

void ${SRV_NAME}::updating() throw ( ::fwTools::Failed )
{

}

void ${SRV_NAME}::updating( fwServices::ObjectMsg::csptr _msg) throw ( ::fwTools::Failed )
{

}

void ${SRV_NAME}::configuring() throw ( ::fwTools::Failed )
{

}



%for i in reversed(NAMESPACE):
} // namespace ${i}

%endfor


