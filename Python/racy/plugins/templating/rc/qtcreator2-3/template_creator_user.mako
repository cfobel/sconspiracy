<?xml version="1.0" encoding="UTF-8"?>
<% import os
configuration = [ 
                ('racy' , PRJ_NAME),
                ('racy/BUILDDEPS=no' , PRJ_NAME + '/BUILDDEPS=no'),
                ('racy/DEBUG=release', PRJ_NAME + ' DEBUG=release'),
                ]%>
<qtcreator>
 <data>
  <variable>GenericProjectManager.GenericProject.Toolchain</variable>
  <value type="QString">ProjectExplorer.ToolChain.Gcc:/usr/bin/g++.x86-linux-generic-elf-64bit.gdb</value>
 </data>
 <data>
  <variable>ProjectExplorer.Project.ActiveTarget</variable>
  <value type="int">0</value>
 </data>
 <data>
  <variable>ProjectExplorer.Project.EditorSettings</variable>
  <valuemap type="QVariantMap">
   <value type="bool" key="EditorConfiguration.AutoIndent">true</value>
   <value type="bool" key="EditorConfiguration.AutoSpacesForTabs">false</value>
   <valuemap type="QVariantMap" key="EditorConfiguration.CodeStyle.0">
    <value type="QString" key="language">Cpp</value>
    <valuemap type="QVariantMap" key="value">
     <value type="bool" key="AlignAssignments">false</value>
     <value type="QString" key="CurrentFallback">CppGlobal</value>
     <value type="bool" key="ExtraPaddingForConditionsIfConfusingAlign">true</value>
     <value type="bool" key="IndentAccessSpecifiers">false</value>
     <value type="bool" key="IndentBlockBody">true</value>
     <value type="bool" key="IndentBlockBraces">false</value>
     <value type="bool" key="IndentBlocksRelativeToSwitchLabels">false</value>
     <value type="bool" key="IndentClassBraces">false</value>
     <value type="bool" key="IndentControlFlowRelativeToSwitchLabels">true</value>
     <value type="bool" key="IndentDeclarationsRelativeToAccessSpecifiers">true</value>
     <value type="bool" key="IndentEnumBraces">false</value>
     <value type="bool" key="IndentFunctionBody">true</value>
     <value type="bool" key="IndentFunctionBraces">false</value>
     <value type="bool" key="IndentNamespaceBody">false</value>
     <value type="bool" key="IndentNamespaceBraces">false</value>
     <value type="bool" key="IndentStatementsRelativeToSwitchLabels">true</value>
     <value type="bool" key="IndentSwitchLabels">false</value>
    </valuemap>
   </valuemap>
   <value type="int" key="EditorConfiguration.CodeStyle.Count">1</value>
   <value type="QByteArray" key="EditorConfiguration.Codec">System</value>
   <value type="QString" key="EditorConfiguration.CurrentFallback">Project</value>
   <value type="int" key="EditorConfiguration.IndentSize">4</value>
   <value type="bool" key="EditorConfiguration.MouseNavigation">true</value>
   <value type="int" key="EditorConfiguration.PaddingMode">1</value>
   <value type="bool" key="EditorConfiguration.ScrollWheelZooming">true</value>
   <value type="bool" key="EditorConfiguration.SmartBackspace">false</value>
   <value type="bool" key="EditorConfiguration.SpacesForTabs">true</value>
   <valuemap type="QVariantMap" key="EditorConfiguration.Tab.0">
    <value type="QString" key="language">Cpp</value>
    <valuemap type="QVariantMap" key="value">
     <value type="bool" key="AutoIndent">true</value>
     <value type="bool" key="AutoSpacesForTabs">false</value>
     <value type="QString" key="CurrentFallback">CppGlobal</value>
     <value type="int" key="IndentSize">4</value>
     <value type="int" key="PaddingMode">1</value>
     <value type="bool" key="SmartBackspace">false</value>
     <value type="bool" key="SpacesForTabs">true</value>
     <value type="int" key="TabKeyBehavior">0</value>
     <value type="int" key="TabSize">8</value>
    </valuemap>
   </valuemap>
   <valuemap type="QVariantMap" key="EditorConfiguration.Tab.1">
    <value type="QString" key="language">QmlJS</value>
    <valuemap type="QVariantMap" key="value">
     <value type="bool" key="AutoIndent">true</value>
     <value type="bool" key="AutoSpacesForTabs">false</value>
     <value type="QString" key="CurrentFallback">QmlJSGlobal</value>
     <value type="int" key="IndentSize">4</value>
     <value type="int" key="PaddingMode">1</value>
     <value type="bool" key="SmartBackspace">false</value>
     <value type="bool" key="SpacesForTabs">true</value>
     <value type="int" key="TabKeyBehavior">0</value>
     <value type="int" key="TabSize">8</value>
    </valuemap>
   </valuemap>
   <value type="int" key="EditorConfiguration.Tab.Count">2</value>
   <value type="int" key="EditorConfiguration.TabKeyBehavior">0</value>
   <value type="int" key="EditorConfiguration.TabSize">4</value>
   <value type="bool" key="EditorConfiguration.UseGlobal">false</value>
   <value type="int" key="EditorConfiguration.Utf8BomBehavior">1</value>
   <value type="bool" key="EditorConfiguration.addFinalNewLine">true</value>
   <value type="bool" key="EditorConfiguration.cleanIndentation">true</value>
   <value type="bool" key="EditorConfiguration.cleanWhitespace">true</value>
   <value type="bool" key="EditorConfiguration.inEntireDocument">false</value>
  </valuemap>
 </data>
 <data>
  <variable>ProjectExplorer.Project.Target.0</variable>
  <valuemap type="QVariantMap">
   <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">Desktop</value>
   <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName"></value>
   <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">GenericProjectManager.GenericTarget</value>
   <value type="int" key="ProjectExplorer.Target.ActiveBuildConfiguration">1</value>
   <value type="int" key="ProjectExplorer.Target.ActiveDeployConfiguration">0</value>
   <value type="int" key="ProjectExplorer.Target.ActiveRunConfiguration">0</value>
<% count = 0%>
%for name, args in configuration:
   <valuemap type="QVariantMap" key="ProjectExplorer.Target.BuildConfiguration.${count}">
    <value type="QString" key="GenericProjectManager.GenericBuildConfiguration.BuildDirectory"></value>
    <value type="QString" key="ProjectExplorer.BuildCOnfiguration.ToolChain">ProjectExplorer.ToolChain.Gcc:/usr/bin/g++.x86-linux-generic-elf-64bit.gdb</value>
    <valuemap type="QVariantMap" key="ProjectExplorer.BuildConfiguration.BuildStepList.0">
     <valuemap type="QVariantMap" key="ProjectExplorer.BuildStepList.Step.0">
      <value type="QString" key="ProjectExplorer.ProcessStep.Arguments">${args}</value>
      <value type="QString" key="ProjectExplorer.ProcessStep.Command">${RACY_CMD}${'.bat' if os.name == 'nt' else ''}</value>
      <value type="bool" key="ProjectExplorer.ProcessStep.Enabled">true</value>
      <value type="QString" key="ProjectExplorer.ProcessStep.WorkingDirectory">%{buildDir}</value>
      <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">${name}</value>
      <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName">${name}</value>
      <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">ProjectExplorer.ProcessStep</value>
     </valuemap>
     <value type="int" key="ProjectExplorer.BuildStepList.StepsCount">1</value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">Compiler</value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName"></value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">ProjectExplorer.BuildSteps.Build</value>
    </valuemap>
    <valuemap type="QVariantMap" key="ProjectExplorer.BuildConfiguration.BuildStepList.1">
     <value type="int" key="ProjectExplorer.BuildStepList.StepsCount">0</value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">Nettoyer</value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName"></value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">ProjectExplorer.BuildSteps.Clean</value>
    </valuemap>
    <value type="int" key="ProjectExplorer.BuildConfiguration.BuildStepListCount">2</value>
    <value type="bool" key="ProjectExplorer.BuildConfiguration.ClearSystemEnvironment">false</value>
    <valuelist type="QVariantList" key="ProjectExplorer.BuildConfiguration.UserEnvironmentChanges"/>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">${name}</value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName">${name}</value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">GenericProjectManager.GenericBuildConfiguration</value>
   </valuemap>
<% count += 1%>
%endfor
   <value type="int" key="ProjectExplorer.Target.BuildConfigurationCount">${len(configuration)}</value>
   <valuemap type="QVariantMap" key="ProjectExplorer.Target.DeployConfiguration.0">
    <valuemap type="QVariantMap" key="ProjectExplorer.BuildConfiguration.BuildStepList.0">
     <value type="int" key="ProjectExplorer.BuildStepList.StepsCount">0</value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">Déploiement</value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName"></value>
     <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">ProjectExplorer.BuildSteps.Deploy</value>
    </valuemap>
    <value type="int" key="ProjectExplorer.BuildConfiguration.BuildStepListCount">1</value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">Pas de déploiement</value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName"></value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">ProjectExplorer.DefaultDeployConfiguration</value>
   </valuemap>
   <value type="int" key="ProjectExplorer.Target.DeployConfigurationCount">1</value>
   <valuemap type="QVariantMap" key="ProjectExplorer.Target.RunConfiguration.0">
    <value type="bool" key="Analyzer.Project.UseGlobal">true</value>
    <value type="bool" key="Analyzer.Project.UseGlobal">true</value>
    <valuelist type="QVariantList" key="Analyzer.Valgrind.AddedSuppressionFiles"/>
    <valuelist type="QVariantList" key="Analyzer.Valgrind.AddedSuppressionFiles"/>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.CollectBusEvents">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.CollectBusEvents">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.CollectSystime">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.CollectSystime">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.EnableBranchSim">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.EnableBranchSim">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.EnableCacheSim">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.EnableCacheSim">false</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.EnableEventToolTips">true</value>
    <value type="bool" key="Analyzer.Valgrind.Callgrind.EnableEventToolTips">true</value>
    <value type="double" key="Analyzer.Valgrind.Callgrind.MinimumCostRatio">0.01</value>
    <value type="double" key="Analyzer.Valgrind.Callgrind.MinimumCostRatio">0.01</value>
    <value type="double" key="Analyzer.Valgrind.Callgrind.VisualisationMinimumCostRatio">10</value>
    <value type="double" key="Analyzer.Valgrind.Callgrind.VisualisationMinimumCostRatio">10</value>
    <value type="bool" key="Analyzer.Valgrind.FilterExternalIssues">true</value>
    <value type="bool" key="Analyzer.Valgrind.FilterExternalIssues">true</value>
    <value type="int" key="Analyzer.Valgrind.NumCallers">25</value>
    <value type="int" key="Analyzer.Valgrind.NumCallers">25</value>
    <valuelist type="QVariantList" key="Analyzer.Valgrind.RemovedSuppressionFiles"/>
    <valuelist type="QVariantList" key="Analyzer.Valgrind.RemovedSuppressionFiles"/>
    <value type="bool" key="Analyzer.Valgrind.TrackOrigins">true</value>
    <value type="bool" key="Analyzer.Valgrind.TrackOrigins">true</value>
    <value type="QString" key="Analyzer.Valgrind.ValgrindExecutable">valgrind</value>
    <value type="QString" key="Analyzer.Valgrind.ValgrindExecutable">valgrind</value>
    <valuelist type="QVariantList" key="Analyzer.Valgrind.VisibleErrorKinds">
     <value type="int">0</value>
     <value type="int">1</value>
     <value type="int">2</value>
     <value type="int">3</value>
     <value type="int">4</value>
     <value type="int">5</value>
     <value type="int">6</value>
     <value type="int">7</value>
     <value type="int">8</value>
     <value type="int">9</value>
     <value type="int">10</value>
     <value type="int">11</value>
     <value type="int">12</value>
     <value type="int">13</value>
     <value type="int">14</value>
    </valuelist>
    <valuelist type="QVariantList" key="Analyzer.Valgrind.VisibleErrorKinds">
     <value type="int">0</value>
     <value type="int">1</value>
     <value type="int">2</value>
     <value type="int">3</value>
     <value type="int">4</value>
     <value type="int">5</value>
     <value type="int">6</value>
     <value type="int">7</value>
     <value type="int">8</value>
     <value type="int">9</value>
     <value type="int">10</value>
     <value type="int">11</value>
     <value type="int">12</value>
     <value type="int">13</value>
     <value type="int">14</value>
    </valuelist>
    <value type="QString" key="ProjectExplorer.CustomExecutableRunConfiguration.Arguments"></value>
    <value type="int" key="ProjectExplorer.CustomExecutableRunConfiguration.BaseEnvironmentBase">2</value>
    <value type="QString" key="ProjectExplorer.CustomExecutableRunConfiguration.Executable"></value>
    <value type="bool" key="ProjectExplorer.CustomExecutableRunConfiguration.UseTerminal">false</value>
    <valuelist type="QVariantList" key="ProjectExplorer.CustomExecutableRunConfiguration.UserEnvironmentChanges"/>
    <value type="QString" key="ProjectExplorer.CustomExecutableRunConfiguration.WorkingDirectory">%{buildDir}</value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.DefaultDisplayName">Exécutable personnalisé</value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.DisplayName"></value>
    <value type="QString" key="ProjectExplorer.ProjectConfiguration.Id">ProjectExplorer.CustomExecutableRunConfiguration</value>
    <value type="uint" key="RunConfiguration.QmlDebugServerPort">3768</value>
    <value type="bool" key="RunConfiguration.UseCppDebugger">true</value>
    <value type="bool" key="RunConfiguration.UseQmlDebugger">false</value>
    <value type="bool" key="RunConfiguration.UseQmlDebuggerAuto">false</value>
   </valuemap>
   <value type="int" key="ProjectExplorer.Target.RunConfigurationCount">1</value>
  </valuemap>
 </data>
 <data>
  <variable>ProjectExplorer.Project.TargetCount</variable>
  <value type="int">1</value>
 </data>
 <data>
  <variable>ProjectExplorer.Project.Updater.EnvironmentId</variable>
  <value type="QString">{9d949d86-d01d-4f09-b989-ea483233bbf0}</value>
 </data>
 <data>
  <variable>ProjectExplorer.Project.Updater.FileVersion</variable>
  <value type="int">10</value>
 </data>
</qtcreator>
