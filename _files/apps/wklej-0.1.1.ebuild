# Copyright 1999-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

DESCRIPTION="a wklej.org submitter"
HOMEPAGE="http://wklej.org"
SRC_URI="${HOMEPAGE}/m/apps/wklej-${PV}.tar.gz"
RESTRICT="nomirror"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~x86 ~amd64"
IUSE=""

DEPEND=""
RDEPEND="dev-lang/python"

src_install() {
    dobin ${WORKDIR}/${P}.py
    dosym ${P}.py /usr/bin/${PN}
}
