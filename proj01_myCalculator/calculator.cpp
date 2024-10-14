#include "calculator.h"

Calculator::Calculator(QWidget *parent)
        : QWidget(parent), display(new QLineEdit(this)), layout(new QGridLayout(this)) {
    createButtons(); // 初始化按钮
    connectSignalsToSlots(); // 连接信号与槽

    // 设置默认布局
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->addWidget(display);
    mainLayout->addLayout(layout);
    setLayout(mainLayout);
}

Calculator::~Calculator() {}

void Calculator::createButtons() {
    QStringList buttons = {
            "清空", "÷", "×", "退格",
            "7", "8", "9", "-",
            "4", "5", "6", "+",
            "1", "2", "3", "=",
            "0"
    };

    int row = 1, col = 0;
    for (const QString &buttonText : buttons) {
        if (col == 4) {
            col = 0;
            row++;
        }
        QPushButton *button = createButton(buttonText, SLOT(buttonClicked()));
        layout->addWidget(button, row, col++);
    }
}

QPushButton* Calculator::createButton(const QString &text, const char *member) {
    QPushButton *button = new QPushButton(text);
    connect(button, SIGNAL(clicked()), this, member);
    return button;
}

void Calculator::connectSignalsToSlots() {
    // 连接按钮信号到槽
}

void Calculator::digitClicked() {
    // 数字按钮被点击后的处理逻辑
}

void Calculator::operatorClicked() {
    // 操作符按钮被点击后的处理逻辑
}

void Calculator::clearClicked() {
    // 清除按钮被点击后的处理逻辑
}

void Calculator::backspaceClicked() {
    // 退格按钮被点击后的处理逻辑
}

void Calculator::equalClicked() {
    // 等号按钮被点击后的处理逻辑
}
