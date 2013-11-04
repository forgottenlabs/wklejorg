# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/app-text/wklej/wklej-0.1.6.ebuild,v 1.3 2009/02/24 21:03:16 mr_bones_ Exp $

EAPI=2

inherit eutils

DESCRIPTION="A wklej.org submitter"
HOMEPAGE="http://wklej.org"
SRC_URI="http://wklej.org/m/apps/wklej-${PV}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64 ~x86 ~x86-fbsd"
IUSE="+vim"

DEPEND="${RDEPEND}"
RDEPEND="dev-lang/python
	vim? ( app-editors/vim[python] )"

src_install() {
	if use vim; then
		insinto /usr/share/vim/vimfiles/plugin
		doins "${WORKDIR}"/${PN}.vim
	fi

	dobin "${WORKDIR}"/${PN}
	dodoc "${WORKDIR}"/README
	dodoc "${WORKDIR}"/wklejrc

    elog "A lot of changes in 0.2.0 version"
    elog "Check out the README file in /usr/share/doc/${PN}-${PV}/README"
    elog "Example of .wklejrc file /usr/share/doc/${PN}-${PV}/wklejrc"
}

