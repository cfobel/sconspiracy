<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?fileVersion 4.0.0?>

<%
import os

if os.name == "nt":
    EXT=".bat"
else:
    EXT=""

CONFIG = project.get("CONFIG")

LIST_TARGET = [
                {'name':"racy",
                 'cmd' : RACY_CMD + EXT,
                 'args': ["CONFIG=" +CONFIG],
                 'target':PRJ_NAME,
                 'target_args':[''],
                 },
                {'name':"racy BUILDDEPS=no",
                 'cmd' : RACY_CMD + EXT,
                 'args':["BUILDDEPS=no", "CONFIG=" +CONFIG],
                 'target':PRJ_NAME,
                 'target_args':'',
                 },
                {'name':"racy DEBUG=release",
                 'cmd' : RACY_CMD + EXT,
                 'args':["DEBUG=release", "CONFIG=" +CONFIG],
                 'target':PRJ_NAME,
                 'target_args':[''],
                 },
                {'name':"racy doxygen",
                 'cmd' : RACY_CMD + EXT,
                 'args':["CONFIG=" +CONFIG],
                 'target':PRJ_NAME,
                 'target_args':['DOX=yes'],
                 },
                {'name':"racy cppunit",
                 'cmd' : RACY_CMD + EXT,
                 'args':["CONFIG=" +CONFIG],
                 'target':PRJ_NAME,
                 'target_args':['CPPUNIT=exec','CPPUNIT_RUN=yes'],
                 },
              ]

%>
<cproject storage_type_id="org.eclipse.cdt.core.XmlProjectDescriptionStorage">
    <storageModule moduleId="org.eclipse.cdt.core.settings">
        <cconfiguration id="0.945266578">
            <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="0.945266578" moduleId="org.eclipse.cdt.core.settings" name="racy BUILDDEPS=no">
                <externalSettings/>
                <extensions>
                    <extension id="org.eclipse.cdt.core.VCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                </extensions>
            </storageModule>
            <storageModule moduleId="cdtBuildSystem" version="4.0.0">
                <configuration artifactName="${PRJ_USER_FORMAT}" buildProperties="" description="" id="0.945266578" name="racy BUILDDEPS=no" parent="org.eclipse.cdt.build.core.prefbase.cfg">
                    <folderInfo id="0.945266578." name="/" resourcePath="">
                        <toolChain id="org.eclipse.cdt.build.core.prefbase.toolchain.671624611" name="No ToolChain" resourceTypeBasedDiscovery="false" superClass="org.eclipse.cdt.build.core.prefbase.toolchain">
                            <targetPlatform id="org.eclipse.cdt.build.core.prefbase.toolchain.671624611.1182702742" name=""/>
                            <builder cleanBuildTarget="-c ${PRJ_NAME}" command="${RACY_CMD}${EXT}" id="org.eclipse.cdt.build.core.settings.default.builder.377367477" incrementalBuildTarget="${PRJ_NAME} BUILDDEPS=no" keepEnvironmentInBuildfile="false" managedBuildOn="false" name="Gnu Make Builder" superClass="org.eclipse.cdt.build.core.settings.default.builder"/>
                            <tool id="org.eclipse.cdt.build.core.settings.holder.libs.240675590" name="holder for library settings" superClass="org.eclipse.cdt.build.core.settings.holder.libs">
                                <option id="org.eclipse.cdt.build.core.settings.holder.libpaths.2040018006" name="Library Paths" superClass="org.eclipse.cdt.build.core.settings.holder.libpaths" valueType="libPaths">
                                </option>
                            </tool>
                            <tool id="org.eclipse.cdt.build.core.settings.holder.1509269446" name="Assembly" superClass="org.eclipse.cdt.build.core.settings.holder">
                                <inputType id="org.eclipse.cdt.build.core.settings.holder.inType.855471375" languageId="org.eclipse.cdt.core.assembly" languageName="Assembly" sourceContentType="org.eclipse.cdt.core.asmSource" superClass="org.eclipse.cdt.build.core.settings.holder.inType"/>
                            </tool>
                            <tool id="org.eclipse.cdt.build.core.settings.holder.1575943659" name="GNU C++" superClass="org.eclipse.cdt.build.core.settings.holder">
                                <option id="org.eclipse.cdt.build.core.settings.holder.incpaths.1251103639" superClass="org.eclipse.cdt.build.core.settings.holder.incpaths" valueType="includePath">
%for i in DEPS_INCLUDES:
                                    <listOptionValue builtIn="false" value="${i}"/>
%endfor
                                </option>
                                <inputType id="org.eclipse.cdt.build.core.settings.holder.inType.57575828" languageId="org.eclipse.cdt.core.g++" languageName="GNU C++" sourceContentType="org.eclipse.cdt.core.cxxSource,org.eclipse.cdt.core.cxxHeader" superClass="org.eclipse.cdt.build.core.settings.holder.inType"/>
                            </tool>
                            <tool id="org.eclipse.cdt.build.core.settings.holder.746746138" name="GNU C" superClass="org.eclipse.cdt.build.core.settings.holder">
                                <inputType id="org.eclipse.cdt.build.core.settings.holder.inType.538761431" languageId="org.eclipse.cdt.core.gcc" languageName="GNU C" sourceContentType="org.eclipse.cdt.core.cSource,org.eclipse.cdt.core.cHeader" superClass="org.eclipse.cdt.build.core.settings.holder.inType"/>
                            </tool>
                        </toolChain>
                    </folderInfo>
                </configuration>
            </storageModule>
            <storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>
        </cconfiguration>
        <cconfiguration id="0.945266578.837898353.967377430">
            <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="0.945266578.837898353.967377430" moduleId="org.eclipse.cdt.core.settings" name="racy">
                <externalSettings/>
                <extensions>
                    <extension id="org.eclipse.cdt.core.VCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                    <extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>
                </extensions>
            </storageModule>
            <storageModule moduleId="cdtBuildSystem" version="4.0.0">
                <configuration artifactName="${PRJ_USER_FORMAT}" buildProperties="" description="" id="0.945266578.837898353.967377430" name="racy" parent="org.eclipse.cdt.build.core.prefbase.cfg">
                    <folderInfo id="0.945266578.837898353.967377430." name="/" resourcePath="">
                        <toolChain id="org.eclipse.cdt.build.core.prefbase.toolchain.772408819" name="No ToolChain" resourceTypeBasedDiscovery="false" superClass="org.eclipse.cdt.build.core.prefbase.toolchain">
                            <targetPlatform id="org.eclipse.cdt.build.core.prefbase.toolchain.772408819.1751368155" name=""/>
                            <builder cleanBuildTarget="-c ${PRJ_NAME}" command="${RACY_CMD}${EXT}" id="org.eclipse.cdt.build.core.settings.default.builder.1414762219" incrementalBuildTarget="${PRJ_NAME}" keepEnvironmentInBuildfile="false" managedBuildOn="false" name="Gnu Make Builder" superClass="org.eclipse.cdt.build.core.settings.default.builder"/>
                            <tool id="org.eclipse.cdt.build.core.settings.holder.libs.543704817" name="holder for library settings" superClass="org.eclipse.cdt.build.core.settings.holder.libs"/>
                        </toolChain>
                    </folderInfo>
                </configuration>
            </storageModule>
            <storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>
        </cconfiguration>
    </storageModule>
    <storageModule moduleId="cdtBuildSystem" version="4.0.0">
        <project id="${PRJ_NAME}.null.1066214194" name="${PRJ_NAME}"/>
    </storageModule>
    <storageModule moduleId="scannerConfiguration">
        <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId=""/>
        <scannerConfigBuildInfo instanceId="0.945266578">
            <autodiscovery enabled="true" problemReportingEnabled="true" selectedProfileId=""/>
        </scannerConfigBuildInfo>
    </storageModule>
    <storageModule moduleId="refreshScope" versionNumber="1">
        <resource resourceType="PROJECT" workspacePath="/${PRJ_NAME}"/>
    </storageModule>
    <storageModule moduleId="org.eclipse.cdt.make.core.buildtargets">
        <buildTargets>
% for config in LIST_TARGET:
            <target name="${config['name']}" path="" targetID="org.eclipse.cdt.build.MakeTargetBuilder">
                <buildCommand>${config['cmd']}</buildCommand>
                <buildArguments>${' '.join(config['args'])}</buildArguments>
                <buildTarget>${config['target'] + '/' + '/'.join(config['target_args'])}</buildTarget>
                <stopOnError>true</stopOnError>
                <useDefaultCommand>false</useDefaultCommand>
                <runAllBuilders>true</runAllBuilders>
            </target>
%endfor
             </buildTargets>
    </storageModule>
</cproject>
