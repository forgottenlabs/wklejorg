# Copyright 1999-2008 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: 

DESCRIPTION="A wklej.org submitter"
HOMEPAGE="http://wklej.org"
SRC_URI="http://wklej.org/m/apps/wklej-${PV}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~x86 ~amd64"
IUSE="vim"

DEPEND="${RDEPEND}"
RDEPEND="dev-lang/python
    vim? ( app-editors/vim )"

pkg_setup() {
    if use vim; then
	build_with_use app-editors/vim python || die "app-editors/vim must be compiled with USE=python"
    fi
}

src_install() {
    if use vim; then
	cp ${WORKDIR}/wklej.vim /usr/share/vim/vim72/plugin/
    fi
    dobin "${WORKDIR}"/${P}.py
    dosym ${P}.py /usr/bin/${PN}
}


