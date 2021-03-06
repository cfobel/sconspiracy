/* ***** BEGIN LICENSE BLOCK *****
 * FW4SPL - Copyright (C) IRCAD, 2009-2010.
 * Distributed under the terms of the GNU Lesser General Public License (LGPL) as
 * published by the Free Software Foundation.
 * ****** END LICENSE BLOCK ****** */
<% 
import os
import os.path
import sys
    


PATH = SRV_SPLITTED_PATH
print PATH
HEADER_GUARD = '_' + '_'.join(PATH) +'_'+SRV_NAME+ '_HPP_'
HEADER_GUARD = HEADER_GUARD.upper()

NAMESPACE = [PRJ_NAME]
NAMESPACE.extend(PATH)


%>

#ifndef ${HEADER_GUARD} 
#define ${HEADER_GUARD}

%for i in NAMESPACE:
namespace ${i}
{

%endfor


class ${PRJ_NAME}_CLASS_API ${SRV_NAME} : public /* SrvSuperClass */
{

public:
    fwCoreServiceClassDefinitionsMacro ( (${SRV_NAME})(/* SrvSuperclass */) ) ;

    ${SRV_NAME}_API ${SRV_NAME}();


    ${SRV_NAME}_API virtual void starting()    throw ( ::fwTools::Failed );
    ${SRV_NAME}_API virtual void stopping()    throw ( ::fwTools::Failed );
    ${SRV_NAME}_API virtual void updating()    throw ( ::fwTools::Failed );
    ${SRV_NAME}_API virtual void updating( fwServices::ObjectMsg::csptr _msg ) throw ( ::fwTools::Failed );
    ${SRV_NAME}_API virtual void configuring() throw ( ::fwTools::Failed );

};



%for i in reversed(NAMESPACE):
} // namespace ${i}

%endfor

#endif /*${HEADER_GUARD}*/

