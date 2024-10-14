#include <QApplication>
#include "calculator.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);     // 创建应用程序对象
    Calculator calculator;            // 创建 Calculator 对象
    calculator.setWindowTitle("MyCalculator");  // 设置窗口标题
    calculator.show();                // 显示主窗口

    return app.exec();    // 运行应用程序事件循环
}
