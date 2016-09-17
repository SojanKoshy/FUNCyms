"""
**** Scripted by Antony Silvester  - antony.silvester@huawei.com ******


This Test check the YMS functionality for NB and SB

List of test cases:
CASE1: Compile ONOS and push it to the test machines
CASE2:
CASE3:
Case4: Uninstalling the app
"""
class FUNCyms:

    def __init__( self ):
        self.default = ''


    def CASE1( self, main ):
        """
        CASE1 is to compile ONOS and push it to the test machines

        Startup sequence:
        cell <name>
        onos-verify-cell
        NOTE: temporary - onos-remove-raft-logs
        onos-uninstall
        git pull Onos-Yang-Tools
        mvn clean install
        git pull Yms
        mvn clean install
        git pull restconf
        mvn clean install
        git pull Ymstest[Test Application]
        mvn clean install
        git pull onos
        mvn clean install
        onos-package
        onos-install -f
        onos-wait-for-start
        start cli sessions
        start yms, restconf and ymstest apps
        """

        import os
        import imp
        import re
        
        main.log.info( "ONOS Single node start " )
        main.case( "Setting up test environment" )
        main.caseExplanation = "Setup the test environment including " +\
                                "installing ONOS, start ONOS."

        PULLCODE = False
        if main.params[ 'GIT' ][ 'pull' ] == 'True':
            PULLCODE = True
        gitBranch = main.params[ 'GIT' ][ 'branch' ]

        onosYangToolsUrl = main.params[ 'GIT' ][ 'onosYangToolsUrl' ]
        ymsUrl = main.params[ 'GIT' ][ 'ymsUrl' ]
        restconfUrl = main.params[ 'GIT' ][ 'restconfUrl' ]
        ymstestUrl = main.params[ 'GIT' ][ 'ymstestUrl' ]

        forceBuild = False        
        if main.params[ 'GIT' ][ 'forceBuild' ] == 'True':
            forceBuild = True
            
        cellName = main.params[ 'ENV' ][ 'cellName' ]
        ipList = os.getenv( main.params[ 'CTRL' ][ 'ip1' ] )


        main.testOnDirectory = re.sub( "(/tests)$", "", main.testDir )
        main.dependencyPath = main.testOnDirectory + \
                                  main.params[ 'DEPENDENCY' ][ 'path' ]

        wrapperFile1 = main.params[ 'DEPENDENCY' ][ 'wrapper1' ]
        main.ymsFunction = imp.load_source( wrapperFile1,
                                            main.dependencyPath +
                                            wrapperFile1 +
                                            ".py" )

        main.log.info( "Removing raft logs" )
        main.ONOSbench.onosRemoveRaftLogs()

        main.CLIs = []
        main.nodes = []
        main.numCtrls= 1

        for i in range( 1, main.numCtrls + 1 ):
            try:
                main.CLIs.append( getattr( main, 'ONOScli' + str( i ) ) )
                main.nodes.append( getattr( main, 'ONOS' + str( i ) ) )
                ipList.append( main.nodes[ -1 ].ip_address )
            except AttributeError:
                break

        main.log.info( "Uninstalling ONOS" )
        for node in main.nodes:
            main.ONOSbench.onosUninstall( node.ip_address )

        main.step( "Create cell file" )
        cellAppString = main.params[ 'ENV' ][ 'cellApps' ]

        main.ONOSbench.createCellFile( main.ONOSbench.ip_address, cellName,
                                       main.ONOSbench.ip_address,
                                       cellAppString, ipList )

        main.step( "Applying cell variable to environment" )
        cellResult = main.ONOSbench.setCell( cellName )

        verifyResult = main.ONOSbench.verifyCell()

        # Make sure ONOS process is not running
        main.log.info( "Killing any ONOS processes" )
        killResults = main.TRUE
        for node in main.nodes:
            killed = main.ONOSbench.onosKill( node.ip_address )
            killResults = killResults and killed

        # Git clone all the dependent apps and clean install
        appsPath = main.dependencyPath + 'apps'        
        main.step( "Git clone and build " + onosYangToolsUrl )
        main.ymsFunction.gitCloneAndBuild( main, appsPath, onosYangToolsUrl,
                                           forceBuild )

        main.step( "Git clone and build " + ymsUrl )
        main.ymsFunction.gitCloneAndBuild( main, appsPath, ymsUrl,
                                           forceBuild )

        main.step( "Git clone and build " + restconfUrl )
        main.ymsFunction.gitCloneAndBuild( main, appsPath, restconfUrl,
                                           forceBuild )

        main.step( "Git clone and build " + ymstestUrl )
        main.ymsFunction.gitCloneAndBuild( main, appsPath, ymstestUrl,
                                           forceBuild )

        cleanInstallResult = main.TRUE
        gitPullResult = main.FALSE
        main.step( "Git checkout and pull" + gitBranch )
        if PULLCODE:
            main.ONOSbench.gitCheckout( gitBranch )
            gitPullResult = main.ONOSbench.gitPull()
            # values of 1 or 3 are good
            utilities.assert_lesser( expect=0, actual=gitPullResult,
                                      onpass="Git pull successful",
                                      onfail="Git pull failed" )

        #main.ONOSbench.getVersion( report=True )

        main.step( "Using mvn clean install" )
        cleanInstallResult = main.TRUE
        if PULLCODE and gitPullResult == main.TRUE:
            cleanInstallResult = main.ONOSbench.cleanInstall()
        else:
            main.log.warn( "Did not pull new code so skipping mvn" +
                           "clean install" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cleanInstallResult,
                                 onpass="MCI successful",
                                 onfail="MCI failed" )

        main.step( "Creating ONOS package" )
        packageResult = main.ONOSbench.buckBuild()
        utilities.assert_equals( expect=main.TRUE,
                                     actual=packageResult,
                                     onpass="Successfully created ONOS package",
                                     onfail="Failed to create ONOS package" )

        main.step( "Installing ONOS package" )
        onosInstallResult = main.ONOSbench.onosInstall(
                options="-f", node=main.nodes[0].ip_address )
        utilities.assert_equals( expect=main.TRUE, actual=onosInstallResult,
                                 onpass="ONOS install successful",
                                 onfail="ONOS install failed" )

        main.step( "Checking if ONOS is up yet" )
        print main.nodes[0].ip_address
        for i in range( 2 ):
            onos1Isup = main.ONOSbench.isup( main.nodes[0].ip_address )
            if onos1Isup:
                break
        utilities.assert_equals( expect=main.TRUE, actual=onos1Isup,
                                 onpass="ONOS startup successful",
                                 onfail="ONOS startup failed" )
        main.step( "Starting ONOS CLI sessions" )
        print main.nodes[0].ip_address
        cliResults = main.ONOScli1.startOnosCli( main.nodes[0].ip_address )
        utilities.assert_equals( expect=main.TRUE, actual=cliResults,
                                 onpass="ONOS cli startup successful",
                                 onfail="ONOS cli startup failed" )

        main.step( "App Ids check" )
        appCheck = main.ONOScli1.appToIDCheck()

        if appCheck !=main.TRUE:
            main.log.warn( main.CLIs[0].apps() )
            main.log.warn( main.CLIs[0].appIDs() )
            utilities.assert_equals( expect=main.TRUE, actual=appCheck,
                                 onpass="App Ids seem to be correct",
                                 onfail="Something is wrong with app Ids" )
        if cliResults == main.FALSE:
            main.log.error( "Failed to start ONOS,stopping test" )
            main.cleanup()
            main.exit()

