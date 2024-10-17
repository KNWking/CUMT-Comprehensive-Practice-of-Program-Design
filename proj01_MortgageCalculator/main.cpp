#include <QApplication>
#include <QMainWindow>
#include "MortgageCalculator.h"

int main(int argc, char *argv[]) {
    // 创建QApplication对象
    QApplication app(argc, argv);

    // 创建主窗口
    MortgageCalculator mortgageCalculator;

    // 显示主窗口
    mortgageCalculator.show();

    // 进入应用程序的事件循环
    return a.exec();
}
