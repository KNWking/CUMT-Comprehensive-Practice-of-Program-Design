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
    QString buttonLabels[5][4] = {
            {"清空", "退格", "",  ""},
            {"7",    "8",    "9", "-"},
            {"4",    "5",    "6", "+"},
            {"1",    "2",    "3", "×"},
            {"0",    ".",    "÷", "="}
    };
    const char *buttonSlots[5][4] = {
            {SLOT(on_op_AC_clicked()), SLOT(on_op_del_clicked()), nullptr, nullptr},
            {SLOT(on_digit_clicked()), SLOT(on_digit_clicked()),  SLOT(on_digit_clicked()),  SLOT(on_op_sub_clicked())},
            {SLOT(on_digit_clicked()), SLOT(on_digit_clicked()),  SLOT(on_digit_clicked()),  SLOT(on_op_add_clicked())},
            {SLOT(on_digit_clicked()), SLOT(on_digit_clicked()),  SLOT(on_digit_clicked()),  SLOT(on_op_mul_clicked())},
            {SLOT(on_digit_clicked()), SLOT(on_op_pnt_clicked()), SLOT(on_op_dvd_clicked()), SLOT(on_op_eqa_clicked())}
    };

    QString opLabels[4][1] = {
            {"sqrt"},
            {"%"},
            {"1/x"},
            {""}
    };
    const char *opSlots[4][1] = {
            {SLOT(on_op_sqrt_clicked())},
            {SLOT(on_op_percent_clicked())},
            {SLOT(on_op_reciprocal_clicked())},
            {nullptr}
    };

    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (!buttonLabels[i][j].isEmpty() && buttonSlots[i][j] != nullptr) {
                QPushButton *button = createButton(buttonLabels[i][j], buttonSlots[i][j]);
                mainLayout->addWidget(button, i, j);
            }
        }
    }

    for (int i = 1; i <= 3; ++i) {
        for (int j = 3; j < 4; ++j) {
            if (!opLabels[i - 1][0].isEmpty() && opSlots[i - 1][0] != nullptr) {
                QPushButton *button = createButton(opLabels[i - 1][0], opSlots[i - 1][0]);
                mainLayout->addWidget(button, i, j);
            }
        }
    }
}

QPushButton *Calculator::createButton(const QString &text, const char *member) {
    QPushButton *button = new QPushButton(text);
    button->setFixedSize(60, 60);
    connect(button, SIGNAL(clicked()), this, member);
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

void Calculator::on_op_dvd_clicked() { display->insert("/"); }

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
    display->setText(QString::number(sqrt(value)));
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

double Calculator::sqrt(double x) {
    return std::sqrt(x);
}

double Calculator::percent(double x) {
    return x / 100;
}

double Calculator::reciprocal(double x) {
    return x != 0 ? 1 / x : 0;
}
