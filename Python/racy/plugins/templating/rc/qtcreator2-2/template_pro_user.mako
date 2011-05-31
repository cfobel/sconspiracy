<!DOCTYPE QtCreatorProject>
<% 
import os                        
step =  [ ('racy' , PRJ_NAME),
         ('racy/BUILDDEPS=no' , PRJ_NAME + '/BUILDDEPS=no'),
         ('racy/DEBUG=release', PRJ_NAME + ' DEBUG=release'),
       ]
       
NB_STEP = len(step)
COUNT = 0

if os.name == "nt":
    EXT = '.bat'
else:
    EXT=''
%>

<qtcreator>
 <data>
  <variable>ProjectExplorer.Project.ActiveTarget</variable>
  <value type="int">0</value>
 </data>
 <data>
  <variable>ProjectExplorer.Project.EditorSettings</variable>
  <valuemap type="QVariantMap">
   <value key="EditorConfiguration.AutoIndent" type="bool">true</value>
   <value key="EditorConfiguration.AutoSpacesForTabs" type="bool">true</value>
   <value key="EditorConfiguration.Codec" type="QByteArray">System</value>
   <value key="EditorConfiguration.DoubleIndentBlocks" type="bool">false</value>
   <value key="EditorConfiguration.IndentBraces" type="bool">true</value>
   <value key="EditorConfiguration.IndentSize" type="int">4</value>
   <value key="EditorConfiguration.MouseNavigation" type="bool">true</value>
   <value key="EditorConfiguration.PaddingMode" type="int">1</value>
   <value key="EditorConfiguration.ScrollWheelZooming" type="bool">true</value>
   <value key="EditorConfiguration.SmartBackspace" type="bool">false</value>
   <value key="EditorConfiguration.SpacesForTabs" type="bool">true</value>
   <value key="EditorConfiguration.TabKeyBehavior" type="int">0</value>
   <value key="EditorConfiguration.TabSize" type="int">4</value>
   <value key="EditorConfiguration.UseGlobal" type="bool">true</value>
   <value key="EditorConfiguration.Utf8BomBehavior" type="int">1</value>
   <value key="EditorConfiguration.addFinalNewLine" type="bool">true</value>
   <value key="EditorConfiguration.cleanIndentation" type="bool">true</value>
   <value key="EditorConfiguration.cleanWhitespace" type="bool">true</value>
   <value key="EditorConfiguration.inEntireDocument" type="bool">false</value>
  </valuemap>
 </data>
 
 
 <data>
  <variable>ProjectExplorer.Project.Target.0</variable>
  <valuemap type="QVariantMap">
   <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Desktop</value>
   <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">Desktop</value>
   <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">Qt4ProjectManager.Target.DesktopTarget</value>
   <value key="ProjectExplorer.Target.ActiveBuildConfiguration" type="int">1</value>
   <value key="ProjectExplorer.Target.ActiveDeployConfiguration" type="int">0</value>
   <value key="ProjectExplorer.Target.ActiveRunConfiguration" type="int">0</value>




%for name, option in step:
   <valuemap key="ProjectExplorer.Target.BuildConfiguration.${COUNT}" type="QVariantMap">
    <value key="ProjectExplorer.BuildCOnfiguration.ToolChain" type="QString">ProjectExplorer.ToolChain.Msvc:C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\vcvars32.bat..</value>
    <valuemap key="ProjectExplorer.BuildConfiguration.BuildStepList.0" type="QVariantMap">
     <valuemap key="ProjectExplorer.BuildStepList.Step.0" type="QVariantMap">
      <value key="ProjectExplorer.ProcessStep.Arguments" type="QString">${option}</value>
      <value key="ProjectExplorer.ProcessStep.Command" type="QString">${RACY_CMD}${EXT}</value>
      <value key="ProjectExplorer.ProcessStep.Enabled" type="bool">true</value>
      <value key="ProjectExplorer.ProcessStep.WorkingDirectory" type="QString">${RACY_INSTALL_DIR}</value>
      <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">${name}</value>
      <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">${name}</value>
      <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">ProjectExplorer.ProcessStep</value>
     </valuemap>
     <value key="ProjectExplorer.BuildStepList.StepsCount" type="int">1</value>
     <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Compiler</value>
     <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">Compiler</value>
     <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">ProjectExplorer.BuildSteps.Build</value>
    </valuemap>
    <valuemap key="ProjectExplorer.BuildConfiguration.BuildStepList.1" type="QVariantMap">
     <valuemap key="ProjectExplorer.BuildStepList.Step.0" type="QVariantMap">
      <value key="ProjectExplorer.ProcessStep.Arguments" type="QString">-c ${PRJ_NAME}</value>
      <value key="ProjectExplorer.ProcessStep.Command" type="QString">${RACY_CMD}</value>
      <value key="ProjectExplorer.ProcessStep.Enabled" type="bool">true</value>
      <value key="ProjectExplorer.ProcessStep.WorkingDirectory" type="QString">${RACY_INSTALL_DIR}</value>
      <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Clean project</value>
      <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">Clean project</value>
      <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">ProjectExplorer.ProcessStep</value>
     </valuemap>
     <value key="ProjectExplorer.BuildStepList.StepsCount" type="int">1</value>
     <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Clean project</value>
     <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">Clean project</value>
     <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">ProjectExplorer.BuildSteps.Clean</value>
    </valuemap>
    <value key="ProjectExplorer.BuildConfiguration.BuildStepListCount" type="int">2</value>
    <value key="ProjectExplorer.BuildConfiguration.ClearSystemEnvironment" type="bool">false</value>
    <valuelist key="ProjectExplorer.BuildConfiguration.UserEnvironmentChanges" type="QVariantList"/>
    <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Qt 4.7.3 for Desktop - MSVC2008 (Qt SDK) Debug</value>
    <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">${name}</value>
    <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">Qt4ProjectManager.Qt4BuildConfiguration</value>
    <value key="Qt4ProjectManager.Qt4BuildConfiguration.BuildConfiguration" type="int">2</value>
    <value key="Qt4ProjectManager.Qt4BuildConfiguration.BuildDirectory" type="QString">${RACY_INSTALL_DIR}</value>
    <value key="Qt4ProjectManager.Qt4BuildConfiguration.QtVersionId" type="int">11</value>
    <value key="Qt4ProjectManager.Qt4BuildConfiguration.ToolChain" type="QString">ProjectExplorer.ToolChain.Msvc:C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\vcvars32.bat..</value>
    <value key="Qt4ProjectManager.Qt4BuildConfiguration.UseShadowBuild" type="bool">true</value>
   </valuemap>
<% COUNT = COUNT + 1 %>
%endfor
<!-- a repete n fois   -->



   <value key="ProjectExplorer.Target.BuildConfigurationCount" type="int">${NB_STEP}</value>
   <valuemap key="ProjectExplorer.Target.DeployConfiguration.0" type="QVariantMap">
    <valuemap key="ProjectExplorer.BuildConfiguration.BuildStepList.0" type="QVariantMap">
     <value key="ProjectExplorer.BuildStepList.StepsCount" type="int">0</value>
     <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Déploiement</value>
     <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString"></value>
     <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">ProjectExplorer.BuildSteps.Deploy</value>
    </valuemap>
    <value key="ProjectExplorer.BuildConfiguration.BuildStepListCount" type="int">1</value>
    <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Pas de déploiement</value>
    <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString"></value>
    <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">ProjectExplorer.DefaultDeployConfiguration</value>
   </valuemap>
   <value key="ProjectExplorer.Target.DeployConfigurationCount" type="int">1</value>
   <valuemap key="ProjectExplorer.Target.RunConfiguration.0" type="QVariantMap">
    <value key="ProjectExplorer.CustomExecutableRunConfiguration.Arguments" type="QString">Bundles\${CALLING_PROJECT_VERSION_NAME}\profile.xml</value>
    <value key="ProjectExplorer.CustomExecutableRunConfiguration.BaseEnvironmentBase" type="int">2</value>
    <value key="ProjectExplorer.CustomExecutableRunConfiguration.Executable"
    type="QString">${CALLING_TARGET}</value>
    <value key="ProjectExplorer.CustomExecutableRunConfiguration.UseTerminal" type="bool">false</value>
    <valuelist key="ProjectExplorer.CustomExecutableRunConfiguration.UserEnvironmentChanges" type="QVariantList"/>
    <value key="ProjectExplorer.CustomExecutableRunConfiguration.WorkingDirectory" type="QString">${RACY_INSTALL_DIR}</value>
    <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">Exécuter ${PRJ_NAME}</value>
    <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">${PRJ_NAME}</value>
    <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">ProjectExplorer.CustomExecutableRunConfiguration</value>
    <value key="RunConfiguration.QmlDebugServerPort" type="uint">3768</value>
    <value key="RunConfiguration.UseCppDebugger" type="bool">true</value>
    <value key="RunConfiguration.UseQmlDebugger" type="bool">false</value>
   </valuemap>
   <valuemap key="ProjectExplorer.Target.RunConfiguration.1" type="QVariantMap">
    <value key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName" type="QString">${PRJ_NAME}</value>
    <value key="ProjectExplorer.ProjectConfiguration.DisplayName" type="QString">${PRJ_NAME}</value>
    <value key="ProjectExplorer.ProjectConfiguration.Id" type="QString">Qt4ProjectManager.Qt4RunConfiguration</value>
    <value key="Qt4ProjectManager.Qt4RunConfiguration.BaseEnvironmentBase" type="int">2</value>
    <value key="Qt4ProjectManager.Qt4RunConfiguration.CommandLineArguments" type="QString"></value>
    <value key="Qt4ProjectManager.Qt4RunConfiguration.ProFile" type="QString">${PRJ_NAME}.pro</value>
    <value key="Qt4ProjectManager.Qt4RunConfiguration.UseDyldImageSuffix" type="bool">false</value>
    <value key="Qt4ProjectManager.Qt4RunConfiguration.UseTerminal" type="bool">false</value>
    <valuelist key="Qt4ProjectManager.Qt4RunConfiguration.UserEnvironmentChanges" type="QVariantList"/>
    <value key="Qt4ProjectManager.Qt4RunConfiguration.UserWorkingDirectory" type="QString"></value>
    <value key="RunConfiguration.QmlDebugServerPort" type="uint">3768</value>
    <value key="RunConfiguration.UseCppDebugger" type="bool">true</value>
    <value key="RunConfiguration.UseQmlDebugger" type="bool">false</value>
   </valuemap>
   <value key="ProjectExplorer.Target.RunConfigurationCount" type="int">2</value>
  </valuemap>
 </data>
 <data>
  <variable>ProjectExplorer.Project.TargetCount</variable>
  <value type="int">1</value>
 </data>
 <data>
  <variable>ProjectExplorer.Project.Updater.FileVersion</variable>
  <value type="int">9</value>
 </data>
</qtcreator>
