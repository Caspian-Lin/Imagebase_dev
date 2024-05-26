/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick 2.15
import QtQuick.Controls 2.15
import Imagebase 1.0

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height
    
    color: Constants.backgroundColor
    
    ToolBar {
        id: toolBar
        x: 0
        y: 0
        width: 1920
        height: 40
        
        ToolButton {
            id: toolButton
            x: 0
            y: 0
            text: qsTr("Tool Button")
        }
    }

    GroupBox {
        id: groupBox
        x: 407
        y: 359
        width: 401
        height: 363
        title: qsTr("Group Box")

        Text {
            id: label
            x: 496
            y: 235
            width: 90
            height: 0
            text: qsTr("Hello Imagebase")
            anchors.top: button.bottom
            font.family: Constants.font.family
            anchors.topMargin: 45
            anchors.horizontalCenter: parent.horizontalCenter

            SequentialAnimation {
                id: animation

                ColorAnimation {
                    id: colorAnimation1
                    target: rectangle
                    property: "color"
                    to: "#2294c6"
                    from: Constants.backgroundColor
                }

                ColorAnimation {
                    id: colorAnimation2
                    target: rectangle
                    property: "color"
                    to: Constants.backgroundColor
                    from: "#2294c6"
                }
            }
        }

        Button {
            id: button
            x: 152
            y: 150
            text: qsTr("Press me")
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -1
            anchors.horizontalCenterOffset: -50
            font.pointSize: 12
            checkable: true
            anchors.horizontalCenter: parent.horizontalCenter

            Connections {
                target: button
                onClicked: animation.start()
            }
        }
    }
    states: [
        State {
            name: "clicked"
            when: button.checked
            
            PropertyChanges {
                target: label
                text: qsTr("Button Checked")
            }
        }
    ]
}
