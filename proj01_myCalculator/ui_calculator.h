/********************************************************************************
** Form generated from reading UI file 'calculator.ui'
**
** Created by: Qt User Interface Compiler version 6.8.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CALCULATOR_H
#define UI_CALCULATOR_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Calculator
{
public:
    QWidget *centralwidget;
    QLineEdit *resultbox;
    QPushButton *num1;
    QPushButton *num2;
    QPushButton *num3;
    QPushButton *num4;
    QPushButton *num5;
    QPushButton *num6;
    QPushButton *num7;
    QPushButton *num8;
    QPushButton *num9;
    QPushButton *num0;
    QPushButton *op_C;
    QPushButton *op_del;
    QPushButton *op_add;
    QPushButton *op_sub;
    QPushButton *op_times;
    QPushButton *op_div;
    QPushButton *op_dot;
    QPushButton *op_equal;
    QPushButton *op_left;
    QPushButton *op_right;

    void setupUi(QMainWindow *Calculator)
    {
        if (Calculator->objectName().isEmpty())
            Calculator->setObjectName("Calculator");
        Calculator->resize(274, 414);
        centralwidget = new QWidget(Calculator);
        centralwidget->setObjectName("centralwidget");
        resultbox = new QLineEdit(centralwidget);
        resultbox->setObjectName("resultbox");
        resultbox->setGeometry(QRect(10, 10, 251, 51));
        QFont font;
        font.setPointSize(18);
        resultbox->setFont(font);
        resultbox->setAlignment(Qt::AlignmentFlag::AlignRight|Qt::AlignmentFlag::AlignTrailing|Qt::AlignmentFlag::AlignVCenter);
        num1 = new QPushButton(centralwidget);
        num1->setObjectName("num1");
        num1->setGeometry(QRect(20, 200, 50, 50));
        num1->setMinimumSize(QSize(50, 50));
        num1->setMaximumSize(QSize(50, 50));
        num1->setFont(font);
        num2 = new QPushButton(centralwidget);
        num2->setObjectName("num2");
        num2->setGeometry(QRect(80, 200, 50, 50));
        num2->setMinimumSize(QSize(50, 50));
        num2->setMaximumSize(QSize(50, 50));
        num2->setFont(font);
        num3 = new QPushButton(centralwidget);
        num3->setObjectName("num3");
        num3->setGeometry(QRect(140, 200, 50, 50));
        num3->setMinimumSize(QSize(50, 50));
        num3->setMaximumSize(QSize(50, 50));
        num3->setFont(font);
        num4 = new QPushButton(centralwidget);
        num4->setObjectName("num4");
        num4->setGeometry(QRect(20, 140, 50, 50));
        num4->setMinimumSize(QSize(50, 50));
        num4->setMaximumSize(QSize(50, 50));
        num4->setFont(font);
        num5 = new QPushButton(centralwidget);
        num5->setObjectName("num5");
        num5->setGeometry(QRect(80, 140, 50, 50));
        num5->setMinimumSize(QSize(50, 50));
        num5->setMaximumSize(QSize(50, 50));
        num5->setFont(font);
        num6 = new QPushButton(centralwidget);
        num6->setObjectName("num6");
        num6->setGeometry(QRect(140, 140, 50, 50));
        num6->setMinimumSize(QSize(50, 50));
        num6->setMaximumSize(QSize(50, 50));
        num6->setFont(font);
        num7 = new QPushButton(centralwidget);
        num7->setObjectName("num7");
        num7->setGeometry(QRect(20, 80, 50, 50));
        num7->setMinimumSize(QSize(50, 50));
        num7->setMaximumSize(QSize(50, 50));
        num7->setFont(font);
        num8 = new QPushButton(centralwidget);
        num8->setObjectName("num8");
        num8->setGeometry(QRect(80, 80, 50, 50));
        num8->setMinimumSize(QSize(50, 50));
        num8->setMaximumSize(QSize(50, 50));
        num8->setFont(font);
        num9 = new QPushButton(centralwidget);
        num9->setObjectName("num9");
        num9->setGeometry(QRect(140, 80, 50, 50));
        num9->setMinimumSize(QSize(50, 50));
        num9->setMaximumSize(QSize(50, 50));
        num9->setFont(font);
        num0 = new QPushButton(centralwidget);
        num0->setObjectName("num0");
        num0->setGeometry(QRect(140, 260, 50, 50));
        num0->setMinimumSize(QSize(50, 50));
        num0->setMaximumSize(QSize(50, 50));
        num0->setFont(font);
        op_C = new QPushButton(centralwidget);
        op_C->setObjectName("op_C");
        op_C->setGeometry(QRect(20, 320, 50, 50));
        op_C->setMinimumSize(QSize(50, 50));
        op_C->setMaximumSize(QSize(50, 50));
        QFont font1;
        font1.setPointSize(12);
        op_C->setFont(font1);
        op_del = new QPushButton(centralwidget);
        op_del->setObjectName("op_del");
        op_del->setGeometry(QRect(80, 320, 50, 50));
        op_del->setMinimumSize(QSize(50, 50));
        op_del->setMaximumSize(QSize(50, 50));
        op_del->setFont(font1);
        op_add = new QPushButton(centralwidget);
        op_add->setObjectName("op_add");
        op_add->setGeometry(QRect(200, 80, 50, 50));
        op_add->setMinimumSize(QSize(50, 50));
        op_add->setMaximumSize(QSize(50, 50));
        QFont font2;
        font2.setPointSize(20);
        op_add->setFont(font2);
        op_sub = new QPushButton(centralwidget);
        op_sub->setObjectName("op_sub");
        op_sub->setGeometry(QRect(200, 140, 50, 50));
        op_sub->setMinimumSize(QSize(50, 50));
        op_sub->setMaximumSize(QSize(50, 50));
        op_sub->setFont(font2);
        op_times = new QPushButton(centralwidget);
        op_times->setObjectName("op_times");
        op_times->setGeometry(QRect(200, 200, 50, 50));
        op_times->setMinimumSize(QSize(50, 50));
        op_times->setMaximumSize(QSize(50, 50));
        op_times->setFont(font2);
        op_div = new QPushButton(centralwidget);
        op_div->setObjectName("op_div");
        op_div->setGeometry(QRect(200, 260, 50, 50));
        op_div->setMinimumSize(QSize(50, 50));
        op_div->setMaximumSize(QSize(50, 50));
        op_div->setFont(font2);
        op_dot = new QPushButton(centralwidget);
        op_dot->setObjectName("op_dot");
        op_dot->setGeometry(QRect(140, 320, 50, 50));
        op_dot->setMinimumSize(QSize(50, 50));
        op_dot->setMaximumSize(QSize(50, 50));
        op_dot->setFont(font2);
        op_equal = new QPushButton(centralwidget);
        op_equal->setObjectName("op_equal");
        op_equal->setGeometry(QRect(200, 320, 50, 50));
        op_equal->setMinimumSize(QSize(50, 50));
        op_equal->setMaximumSize(QSize(50, 50));
        op_equal->setFont(font2);
        op_left = new QPushButton(centralwidget);
        op_left->setObjectName("op_left");
        op_left->setGeometry(QRect(20, 260, 50, 50));
        op_left->setMinimumSize(QSize(50, 50));
        op_left->setMaximumSize(QSize(50, 50));
        op_left->setFont(font);
        op_right = new QPushButton(centralwidget);
        op_right->setObjectName("op_right");
        op_right->setGeometry(QRect(80, 260, 50, 50));
        op_right->setMinimumSize(QSize(50, 50));
        op_right->setMaximumSize(QSize(50, 50));
        op_right->setFont(font);
        Calculator->setCentralWidget(centralwidget);

        retranslateUi(Calculator);

        QMetaObject::connectSlotsByName(Calculator);
    } // setupUi

    void retranslateUi(QMainWindow *Calculator)
    {
        Calculator->setWindowTitle(QCoreApplication::translate("Calculator", "MainWindow", nullptr));
        resultbox->setText(QCoreApplication::translate("Calculator", "\350\257\267\350\276\223\345\205\245\350\246\201\350\256\241\347\256\227\347\232\204\345\274\217\345\255\220", nullptr));
        num1->setText(QCoreApplication::translate("Calculator", "1", nullptr));
        num2->setText(QCoreApplication::translate("Calculator", "2", nullptr));
        num3->setText(QCoreApplication::translate("Calculator", "3", nullptr));
        num4->setText(QCoreApplication::translate("Calculator", "4", nullptr));
        num5->setText(QCoreApplication::translate("Calculator", "5", nullptr));
        num6->setText(QCoreApplication::translate("Calculator", "6", nullptr));
        num7->setText(QCoreApplication::translate("Calculator", "7", nullptr));
        num8->setText(QCoreApplication::translate("Calculator", "8", nullptr));
        num9->setText(QCoreApplication::translate("Calculator", "9", nullptr));
        num0->setText(QCoreApplication::translate("Calculator", "0", nullptr));
        op_C->setText(QCoreApplication::translate("Calculator", "\346\270\205\347\251\272", nullptr));
        op_del->setText(QCoreApplication::translate("Calculator", "\351\200\200\346\240\274", nullptr));
        op_add->setText(QCoreApplication::translate("Calculator", "+", nullptr));
        op_sub->setText(QCoreApplication::translate("Calculator", "-", nullptr));
        op_times->setText(QCoreApplication::translate("Calculator", "\303\227", nullptr));
        op_div->setText(QCoreApplication::translate("Calculator", "\303\267", nullptr));
        op_dot->setText(QCoreApplication::translate("Calculator", ".", nullptr));
        op_equal->setText(QCoreApplication::translate("Calculator", "=", nullptr));
        op_left->setText(QCoreApplication::translate("Calculator", "(", nullptr));
        op_right->setText(QCoreApplication::translate("Calculator", ")", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Calculator: public Ui_Calculator {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CALCULATOR_H
