#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <QMainWindow>
#include <stack>
#include <cmath>
#include <limits>
#include <QString>
#include <string>

QT_BEGIN_NAMESPACE
namespace Ui {
    class Calculator;
}
QT_END_NAMESPACE

class Calculator : public QMainWindow {
Q_OBJECT

public:
    Calculator(QWidget *parent = nullptr);

    ~Calculator();

private slots:

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

    void on_op_add_clicked();

    void on_op_sub_clicked();

    void on_op_times_clicked();

    void on_op_div_clicked();

    void on_op_equal_clicked();

    void on_op_C_clicked();

    void on_op_dot_clicked();

    void on_op_left_clicked();

    void on_op_right_clicked();

    void on_op_del_clicked();


private:
    // 界面对象和核心功能对象。
    Ui::Calculator *ui;

    QString rowFormula = "";

    int priority(int state, char a);

    double calculate(char op, double op1, double op2);

    void processCalculation(QString &rowFormula);

    // 辅助函数。
    bool ifBracketsBalanced(const std::string &str);

    bool hasConsecutiveOperators(const std::string &s);

    bool isOperator(char c);

    void setError(const std::string &message);


};

#endif // CALCULATOR_H
