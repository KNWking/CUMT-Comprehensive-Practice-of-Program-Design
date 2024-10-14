#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <QMainWindow>
#include <QLineEdit>
#include <QGridLayout>
#include <QPushButton>
#include <stack>

class Calculator : public QMainWindow {
Q_OBJECT

public:
    explicit Calculator(QWidget *parent = nullptr);

    ~Calculator();

private slots:

    void on_digit_clicked();

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
    int priority(char op);

    bool calculate(double op1, char op, double op2, double &result);

    void processCalculation();

    QString currentExpression;
    QLineEdit *display;
    QGridLayout *mainLayout;

    void createButtons();

    QPushButton *createButton(const QString &text, const char *member);
};

#endif // CALCULATOR_H
