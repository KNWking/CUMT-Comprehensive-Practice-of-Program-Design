#include <QApplication>
#include "MortgageCalculator.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    MortgageCalculator w;
    w.show();
    return QApplication::exec();
}
