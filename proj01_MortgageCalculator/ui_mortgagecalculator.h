/********************************************************************************
** Form generated from reading UI file 'mortgagecalculator.ui'
**
** Created by: Qt User Interface Compiler version 6.8.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MORTGAGECALCULATOR_H
#define UI_MORTGAGECALCULATOR_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MortgageCalculator
{
public:
    QWidget *centralwidget;
    QRadioButton *equalPayment;
    QRadioButton *equalPrincipal;
    QLabel *label;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QPushButton *calculate;
    QPushButton *reset;
    QLineEdit *loanTerm;
    QLineEdit *loanAmount;
    QLineEdit *interestRate;
    QLineEdit *monthlyPayment;
    QLineEdit *totalInterest;
    QLineEdit *totalPayment;

    void setupUi(QMainWindow *MortgageCalculator)
    {
        if (MortgageCalculator->objectName().isEmpty())
            MortgageCalculator->setObjectName("MortgageCalculator");
        MortgageCalculator->resize(321, 293);
        centralwidget = new QWidget(MortgageCalculator);
        centralwidget->setObjectName("centralwidget");
        equalPayment = new QRadioButton(centralwidget);
        equalPayment->setObjectName("equalPayment");
        equalPayment->setGeometry(QRect(150, 20, 88, 20));
        QFont font;
        font.setPointSize(10);
        equalPayment->setFont(font);
        equalPrincipal = new QRadioButton(centralwidget);
        equalPrincipal->setObjectName("equalPrincipal");
        equalPrincipal->setGeometry(QRect(230, 20, 88, 20));
        equalPrincipal->setFont(font);
        label = new QLabel(centralwidget);
        label->setObjectName("label");
        label->setGeometry(QRect(30, 20, 71, 21));
        QFont font1;
        font1.setPointSize(12);
        label->setFont(font1);
        label_2 = new QLabel(centralwidget);
        label_2->setObjectName("label_2");
        label_2->setGeometry(QRect(30, 50, 121, 21));
        label_2->setFont(font1);
        label_3 = new QLabel(centralwidget);
        label_3->setObjectName("label_3");
        label_3->setGeometry(QRect(30, 80, 131, 21));
        label_3->setFont(font1);
        label_4 = new QLabel(centralwidget);
        label_4->setObjectName("label_4");
        label_4->setGeometry(QRect(30, 110, 101, 21));
        label_4->setFont(font1);
        label_5 = new QLabel(centralwidget);
        label_5->setObjectName("label_5");
        label_5->setGeometry(QRect(30, 180, 101, 21));
        label_5->setFont(font1);
        label_6 = new QLabel(centralwidget);
        label_6->setObjectName("label_6");
        label_6->setGeometry(QRect(30, 210, 101, 21));
        label_6->setFont(font1);
        label_7 = new QLabel(centralwidget);
        label_7->setObjectName("label_7");
        label_7->setGeometry(QRect(30, 240, 101, 21));
        label_7->setFont(font1);
        calculate = new QPushButton(centralwidget);
        calculate->setObjectName("calculate");
        calculate->setGeometry(QRect(70, 140, 80, 21));
        QFont font2;
        font2.setPointSize(11);
        calculate->setFont(font2);
        reset = new QPushButton(centralwidget);
        reset->setObjectName("reset");
        reset->setGeometry(QRect(170, 140, 80, 21));
        reset->setFont(font2);
        loanTerm = new QLineEdit(centralwidget);
        loanTerm->setObjectName("loanTerm");
        loanTerm->setGeometry(QRect(152, 50, 131, 22));
        loanAmount = new QLineEdit(centralwidget);
        loanAmount->setObjectName("loanAmount");
        loanAmount->setGeometry(QRect(152, 80, 131, 22));
        interestRate = new QLineEdit(centralwidget);
        interestRate->setObjectName("interestRate");
        interestRate->setGeometry(QRect(152, 110, 131, 22));
        monthlyPayment = new QLineEdit(centralwidget);
        monthlyPayment->setObjectName("monthlyPayment");
        monthlyPayment->setGeometry(QRect(152, 180, 131, 22));
        totalInterest = new QLineEdit(centralwidget);
        totalInterest->setObjectName("totalInterest");
        totalInterest->setGeometry(QRect(152, 210, 131, 22));
        totalPayment = new QLineEdit(centralwidget);
        totalPayment->setObjectName("totalPayment");
        totalPayment->setGeometry(QRect(152, 240, 131, 22));
        MortgageCalculator->setCentralWidget(centralwidget);

        retranslateUi(MortgageCalculator);

        QMetaObject::connectSlotsByName(MortgageCalculator);
    } // setupUi

    void retranslateUi(QMainWindow *MortgageCalculator)
    {
        MortgageCalculator->setWindowTitle(QCoreApplication::translate("MortgageCalculator", "MortgageCalculator", nullptr));
        equalPayment->setText(QCoreApplication::translate("MortgageCalculator", "\347\255\211\351\242\235\346\234\254\346\201\257", nullptr));
        equalPrincipal->setText(QCoreApplication::translate("MortgageCalculator", "\347\255\211\351\242\235\346\234\254\351\207\221", nullptr));
        label->setText(QCoreApplication::translate("MortgageCalculator", "\350\277\230\346\254\276\346\226\271\345\274\217\357\274\232", nullptr));
        label_2->setText(QCoreApplication::translate("MortgageCalculator", "\350\264\267\346\254\276\345\271\264\351\231\220 (\345\271\264)\357\274\232", nullptr));
        label_3->setText(QCoreApplication::translate("MortgageCalculator", "\350\264\267\346\254\276\351\207\221\351\242\235 (\344\270\207\345\205\203)\357\274\232", nullptr));
        label_4->setText(QCoreApplication::translate("MortgageCalculator", "\350\264\267\346\254\276\345\210\251\347\216\207 (%)\357\274\232", nullptr));
        label_5->setText(QCoreApplication::translate("MortgageCalculator", "\346\234\210\345\235\207\350\277\230\346\254\276 (\345\205\203)\357\274\232", nullptr));
        label_6->setText(QCoreApplication::translate("MortgageCalculator", "\345\210\251\346\201\257\346\200\273\351\242\235 (\345\205\203)\357\274\232", nullptr));
        label_7->setText(QCoreApplication::translate("MortgageCalculator", "\350\277\230\346\254\276\346\200\273\351\242\235 (\345\205\203)\357\274\232", nullptr));
        calculate->setText(QCoreApplication::translate("MortgageCalculator", "\350\256\241  \347\256\227", nullptr));
        reset->setText(QCoreApplication::translate("MortgageCalculator", "\346\270\205\347\251\272", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MortgageCalculator: public Ui_MortgageCalculator {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MORTGAGECALCULATOR_H
