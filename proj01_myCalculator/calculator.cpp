#include "calculator.h"

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
    QString buttons[4][4] = {
            {"7", "8", "9", "+"},
            {"4", "5", "6", "-"},
            {"1", "2", "3", "*"},
            {"0", "C", "=", "/"}
    };

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            QPushButton *button = createButton(buttons[i][j], SLOT(on_digit_clicked()));
            mainLayout->addWidget(button, i, j);
        }
    }
}

QPushButton *Calculator::createButton(const QString &text, const char *member) {
    QPushButton *button = new QPushButton(text);
    button->setFixedSize(40, 40);
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

void Calculator::on_op_eqa_clicked() {
    processCalculation();
}

void Calculator::on_op_AC_clicked() { display->clear(); }

void Calculator::on_op_pnt_clicked() { display->insert("."); }

void Calculator::on_op_lf_clicked() { display->insert("("); }

void Calculator::on_op_rt_clicked() { display->insert(")"); }

void Calculator::on_op_del_clicked() {
    QString text = display->text();
    text.chop(1);
    display->setText(text);
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

double Calculator::calculate(double op1, char op, double op2) {
    switch (op) {
        case '+':
            return op1 + op2;
        case '-':
            return op1 - op2;
        case '*':
            return op1 * op2;
        case '/':
            return op2 != 0 ? op1 / op2 : 0; // 简单处理除零错误
        default:
            return 0;
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
                values.push(calculate(op1, op, op2));
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
        values.push(calculate(op1, op, op2));
    }

    if (!values.empty()) {
        display->setText(QString::number(values.top()));
    }
}
