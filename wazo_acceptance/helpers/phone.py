# Copyright 2025-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod


class Phone(ABC):

    @abstractmethod
    def call(self, exten):
        pass

    @abstractmethod
    def hangup(self):
        pass
