#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <QMainWindow>
#include <QLineEdit>
#include <QGridLayout>
#include <QPushButton>

class Calculator : public QMainWindow {
Q_OBJECT

public:
    explicit Calculator(QWidget *parent = nullptr);

    ~Calculator();

private slots:

    // 数字按钮槽函数
    void on_num0_clicked();

    void on_num1_clicked();

    void on_num2_clicked();

    void on_num3_clicked();

    void on_num4_clicked();

    void on_num5_clicked();

    void on_num6_clicked();

    void on_num7_clicked();

    void on_num8_clicked();

    void on_num9_clicked();

    // 操作按钮槽函数
    void on_op_add_clicked();

    void on_op_sub_clicked();

    void on_op_mul_clicked();

    void on_op_dvd_clicked();

    void on_op_eqa_clicked();

    void on_op_AC_clicked();

    void on_op_pnt_clicked();

    void on_op_lf_clicked();

    void on_op_rt_clicked();

    void on_op_del_clicked();

private:
    // 辅助功能函数
    int priority(int state, char a);

    double calculate(char op, double op1, double op2);

    void processCalculation(QString &expression);

    QString currentExpression; // 当前表达式

    // UI 元素
    QLineEdit *display;
    QGridLayout *mainLayout;

    // 辅助函数
    void createButtons();

    QPushButton *createButton(const QString &text, const char *member);
};

#endif // CALCULATOR_H
