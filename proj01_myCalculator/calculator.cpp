#include "calculator.h"
#include <cmath>

Calculator::Calculator(QWidget *parent)
        : QMainWindow(parent), display(new QLineEdit(this)), mainLayout(new QGridLayout) {
    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    display->setReadOnly(true);
    display->setAlignment(Qt::AlignRight);
    display->setFixedHeight(35);

    QVBoxLayout *layout = new QVBoxLayout;
    layout->addWidget(display);
    layout->addLayout(mainLayout);

    centralWidget->setLayout(layout);

    createButtons();
}

Calculator::~Calculator() {}

void Calculator::createButtons() {
    // 清空和退格按钮
    createButton("清空", SLOT(on_op_AC_clicked()), 0, 0, 1, 1);
    createButton("退格", SLOT(on_op_del_clicked()), 0, 1, 1, 2);

    // 数字按钮和 '.' 按钮
    createButton("7", SLOT(on_digit_clicked()), 1, 0);
    createButton("8", SLOT(on_digit_clicked()), 1, 1);
    createButton("9", SLOT(on_digit_clicked()), 1, 2);
    createButton("-", SLOT(on_op_sub_clicked()), 1, 3);
    createButton("sqrt", SLOT(on_op_sqrt_clicked()), 1, 4);

    createButton("4", SLOT(on_digit_clicked()), 2, 0);
    createButton("5", SLOT(on_digit_clicked()), 2, 1);
    createButton("6", SLOT(on_digit_clicked()), 2, 2);
    createButton("+", SLOT(on_op_add_clicked()), 2, 3);
    createButton("%", SLOT(on_op_percent_clicked()), 2, 4);

    createButton("1", SLOT(on_digit_clicked()), 3, 0);
    createButton("2", SLOT(on_digit_clicked()), 3, 1);
    createButton("3", SLOT(on_digit_clicked()), 3, 2);
    createButton("×", SLOT(on_op_mul_clicked()), 3, 3);
    createButton("1/x", SLOT(on_op_reciprocal_clicked()), 3, 4);

    createButton("0", SLOT(on_digit_clicked()), 4, 0, 1, 2);
    createButton(".", SLOT(on_op_pnt_clicked()), 4, 2);
    createButton("÷", SLOT(on_op_div_clicked()), 4, 3);
    createButton("=", SLOT(on_op_eqa_clicked()), 4, 4);
}

QPushButton *
Calculator::createButton(const QString &text, const char *member, int row, int col, int rowspan, int colspan) {
    QPushButton *button = new QPushButton(text);
    button->setFixedSize(60, 60);
    connect(button, SIGNAL(clicked()), this, member);
    mainLayout->addWidget(button, row, col, rowspan, colspan);
    return button;
}

void Calculator::on_digit_clicked() {
    QPushButton *button = qobject_cast<QPushButton *>(sender());
    if (button) {
        display->insert(button->text());
    }
}

void Calculator::on_op_add_clicked() { display->insert("+"); }

void Calculator::on_op_sub_clicked() { display->insert("-"); }

void Calculator::on_op_mul_clicked() { display->insert("*"); }

void Calculator::on_op_div_clicked() { display->insert("/"); }

void Calculator::on_op_eqa_clicked() { processCalculation(); }

void Calculator::on_op_AC_clicked() { display->clear(); }

void Calculator::on_op_pnt_clicked() { display->insert("."); }

void Calculator::on_op_del_clicked() {
    QString text = display->text();
    text.chop(1);
    display->setText(text);
}

void Calculator::on_op_sqrt_clicked() {
    QString text = display->text();
    double value = text.toDouble();
    display->setText(QString::number(std::sqrt(value)));
}

void Calculator::on_op_percent_clicked() {
    QString text = display->text();
    double value = text.toDouble();
    display->setText(QString::number(value / 100));
}

void Calculator::on_op_reciprocal_clicked() {
    QString text = display->text();
    double value = text.toDouble();
    if (value != 0) {
        display->setText(QString::number(1 / value));
    } else {
        display->setText("Error");
    }
}

int Calculator::priority(char op) {
    switch (op) {
        case '+':
        case '-':
            return 1;
        case '*':
        case '/':
            return 2;
        default:
            return 0;
    }
}

bool Calculator::calculate(double op1, char op, double op2, double &result) {
    switch (op) {
        case '+':
            result = op1 + op2;
            return true;
        case '-':
            result = op1 - op2;
            return true;
        case '*':
            result = op1 * op2;
            return true;
        case '/':
            if (op2 != 0) {
                result = op1 / op2;
                return true;
            } else {
                return false;
            }
        default:
            return false;
    }
}

void Calculator::processCalculation() {
    QString expression = display->text();
    std::stack<double> values;
    std::stack<char> ops;
    QString temp;

    for (int i = 0; i < expression.length(); i++) {
        QChar ch = expression[i];

        if (ch.isDigit() || ch == '.') {
            temp += ch;
        } else {
            if (!temp.isEmpty()) {
                values.push(temp.toDouble());
                temp.clear();
            }

            while (!ops.empty() && priority(ops.top()) >= priority(ch.toLatin1())) {
                double op2 = values.top();
                values.pop();
                double op1 = values.top();
                values.pop();
                char op = ops.top();
                ops.pop();
                double result;
                if (!calculate(op1, op, op2, result)) {
                    display->setText("Error");
                    return;
                }
                values.push(result);
            }
            ops.push(ch.toLatin1());
        }
    }

    if (!temp.isEmpty()) {
        values.push(temp.toDouble());
    }

    while (!ops.empty()) {
        double op2 = values.top();
        values.pop();
        double op1 = values.top();
        values.pop();
        char op = ops.top();
        ops.pop();
        double result;
        if (!calculate(op1, op, op2, result)) {
            display->setText("Error");
            return;
        }
        values.push(result);
    }

    if (!values.empty()) {
        display->setText(QString::number(values.top()));
    }
}
