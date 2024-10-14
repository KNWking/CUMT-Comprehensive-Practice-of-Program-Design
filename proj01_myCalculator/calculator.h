#ifndef PROJ01_MYCALCULATOR_CALCULATOR_H
#define PROJ01_MYCALCULATOR_CALCULATOR_H
// 头文件内容
#include <QWidget>
#include <QLineEdit>
#include <QGridLayout>
#include <QPushButton>
#include <QMainWindow>
#include <QDialog>

class Calculator : public QWidget {
    Q_OBJECT // 支持 Qt 的信号与槽机制

public:
    // 构造函数
    explicit Calculator(QWidget *parent = nullptr);
    // 析构函数
    ~Calculator();

private slots:
    // 数字按钮的槽函数
    void digitClicked();
    // 操作符按钮的槽函数
    void operatorClicked();
    // 清除按钮的槽函数
    void clearClicked();
    // 退格按钮的槽函数
    void backspaceClicked();
    // 等号按钮的槽函数
    void equalClicked();

private:
    QLineEdit *display; // 显示器
    QGridLayout *layout; // 按钮布局
    // 辅助函数，创建按钮并连接到槽
    QPushButton *createButton(const QString &text, const char *member);

    // 初始化并创建按钮
    void createButtons();
    // 连接按钮的信号与槽
    void connectSignalsToSlots();
};

#endif //PROJ01_MYCALCULATOR_CALCULATOR_H
