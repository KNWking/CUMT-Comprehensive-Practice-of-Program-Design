#include "MortgageCalculator.h"
#include "ui_mortgagecalculator.h"

MortgageCalculator::MortgageCalculator(QWidget *parent)
        : QMainWindow(parent), ui(new Ui::MortgageCalculator),
          loanTerm(0), loanAmount(0), interestRate(0), repaymentType(0),
          monthlyPayment(0), totalInterest(0), totalPayment(0) {
    ui->setupUi(this);
    connect(ui->calculate, &QPushButton::clicked, this, &MortgageCalculator::on_calculate_clicked);
    connect(ui->reset, &QPushButton::clicked, this, &MortgageCalculator::on_reset_clicked);
}

MortgageCalculator::~MortgageCalculator() {
    delete ui;
}

void MortgageCalculator::on_calculate_clicked() {
    if (!validateInputs()) {
        return;
    }

    setLoanAmount(ui->loanAmount->text().toDouble());
    setInterestRate(ui->interestRate->text().toDouble());
    setLoanTerm(ui->loanTerm->text().toInt());
    setRepaymentType(ui->equalPayment->isChecked() ? 0 : 1);

    if (repaymentType == 0) {
        calculateEqualPayment();
    } else {
        calculateEqualPrincipal();
    }

    displayResults(monthlyPayment, totalInterest, totalPayment);
}

void MortgageCalculator::on_reset_clicked() {
    resetFields();
}

void MortgageCalculator::setLoanTerm(double years) {
    loanTerm = years;
}

void MortgageCalculator::setLoanAmount(double amount) {
    loanAmount = amount * 10000;
}

void MortgageCalculator::setInterestRate(double rate) {
    interestRate = rate / 100.0; // Convert percentage to decimal
}

void MortgageCalculator::setRepaymentType(int type) {
    repaymentType = type;
}

void MortgageCalculator::calculateEqualPayment() {
    double monthlyRate = interestRate / 12.0;
    int totalMonths = loanTerm * 12;

    monthlyPayment = loanAmount * monthlyRate * std::pow(1 + monthlyRate, totalMonths)
                     / (std::pow(1 + monthlyRate, totalMonths) - 1);

    totalPayment = monthlyPayment * totalMonths;
    totalInterest = totalPayment - loanAmount;
}

void MortgageCalculator::calculateEqualPrincipal() {
    int totalMonths = loanTerm * 12;
    double monthlyPrincipal = loanAmount / totalMonths;
    double totalInterestTemp = 0;
    double totalPaymentTemp = 0;

    for (int month = 0; month < totalMonths; ++month) {
        double remainingBalance = loanAmount - (monthlyPrincipal * month);
        double monthlyInterest = remainingBalance * (interestRate / 12.0);
        totalInterestTemp += monthlyInterest;
        totalPaymentTemp += monthlyPrincipal + monthlyInterest;
    }

    // 每月平均支付钱数。
    monthlyPayment = totalPaymentTemp / totalMonths;
    totalInterest = totalInterestTemp;
    totalPayment = totalPaymentTemp;
}

void MortgageCalculator::displayResults(double monthlyPayment, double totalInterest, double totalPayment) {
    ui->monthlyPayment->setText(QString::number(monthlyPayment, 'f', 2));
    ui->totalInterest->setText(QString::number(totalInterest, 'f', 2));
    ui->totalPayment->setText(QString::number(totalPayment, 'f', 2));
}

void MortgageCalculator::resetFields() {
    ui->loanAmount->clear();
    ui->interestRate->clear();
    ui->loanTerm->clear();
    ui->monthlyPayment->clear();
    ui->totalInterest->clear();
    ui->totalPayment->clear();
    ui->equalPayment->setChecked(true);
}

bool MortgageCalculator::validateInputs() const {
    bool ok;
    double amount = ui->loanAmount->text().toDouble(&ok);
    if (!ok || amount <= 0) {
        QMessageBox::warning(const_cast<MortgageCalculator *>(this), "Invalid Input",
                             "Please enter a valid loan amount.");
        return false;
    }

    double rate = ui->interestRate->text().toDouble(&ok);
    if (!ok || rate <= 0 || rate >= 100) {
        QMessageBox::warning(const_cast<MortgageCalculator *>(this), "Invalid Input",
                             "Please enter a valid interest rate (0-100%).");
        return false;
    }

    int term = ui->loanTerm->text().toInt(&ok);
    if (!ok || term <= 0) {
        QMessageBox::warning(const_cast<MortgageCalculator *>(this), "Invalid Input",
                             "Please enter a valid loan term.");
        return false;
    }

    return true;
}
