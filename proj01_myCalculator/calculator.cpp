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
    // 数字按钮和操作符按钮的初始化及布局
    QString buttons[4][4] = {
            {"7", "8", "9", "+"},
            {"4", "5", "6", "-"},
            {"1", "2", "3", "*"},
            {"0", "C", "=", "/"}
    };

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            QPushButton *button = createButton(buttons[i][j], SLOT(digitClicked()));
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

void Calculator::on_num0_clicked() { display->insert("0"); }

void Calculator::on_num1_clicked() { display->insert("1"); }

void Calculator::on_num2_clicked() { display->insert("2"); }

void Calculator::on_num3_clicked() { display->insert("3"); }

void Calculator::on_num4_clicked() { display->insert("4"); }

void Calculator::on_num5_clicked() { display->insert("5"); }

void Calculator::on_num6_clicked() { display->insert("6"); }

void Calculator::on_num7_clicked() { display->insert("7"); }

void Calculator::on_num8_clicked() { display->insert("8"); }

void Calculator::on_num9_clicked() { display->insert("9"); }

void Calculator::on_op_add_clicked() { display->insert("+"); }

void Calculator::on_op_sub_clicked() { display->insert("-"); }

void Calculator::on_op_mul_clicked() { display->insert("*"); }

void Calculator::on_op_dvd_clicked() { display->insert("/"); }

void Calculator::on_op_eqa_clicked() {
    // 处理等于按钮点击事件实现
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

int Calculator::priority(int state, char a) {
    // 实现表达式优先级
    return 0;
}

double Calculator::calculate(char op, double op1, double op2) {
    // 实现计算逻辑
    return 0.0;
}

void Calculator::processCalculation(QString &expression) {
    // 实现表达式处理
}
