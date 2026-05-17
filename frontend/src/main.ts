import './style.css'

type Country = {
  code: string
  name: string
  stripe_colors: string[]
  total_stickers: number
  owned_stickers: number
  missing_stickers: number
}

type Sticker = {
  id: number
  name: string
  position: string | null
  image_url: string | null
  scarcity: number
  owned: boolean
}

type CountryPage = {
  code: string
  name: string
  stripe_colors: string[]
  stickers: Sticker[]
}

type PackSticker = {
  id: number
  name: string
  country_code: string
  country_name: string
  position: string | null
  image_url: string | null
  is_new: boolean
}

type PackResult = {
  opened: boolean
  remaining_today: number
  stickers: PackSticker[]
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
const collectorSlug = 'demo'
const appRoot = document.querySelector<HTMLDivElement>('#app')

if (!appRoot) {
  throw new Error('Missing app root')
}

const app = appRoot

let countries: Country[] = []
let selectedCountryCode = 'ARG'
let selectedPage: CountryPage | null = null
let lastPack: PackResult | null = null
let loading = true
let notice = ''
let pageTurning = false
let sidebarOpen = true

async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`)
  if (!response.ok) {
    throw new Error(`API ${response.status}`)
  }
  return response.json() as Promise<T>
}

async function apiPost<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, { method: 'POST' })
  if (response.status === 429) {
    const limit = (await response.json()) as { detail: PackResult & { reason: string } }
    notice = limit.detail.reason === 'daily_limit_reached' ? 'Ya abriste los sobres de hoy' : 'Sobre no disponible'
    return limit.detail as T
  }
  if (!response.ok) {
    throw new Error(`API ${response.status}`)
  }
  return response.json() as Promise<T>
}

function countryName(name: string): string {
  return (
    {
      Brazil: 'Brasil',
      France: 'Francia',
    }[name] ?? name
  )
}

function positionName(position: string | null): string {
  if (!position) {
    return 'Plantel'
  }
  return (
    {
      Goalkeeper: 'Arquero',
      Defender: 'Defensor',
      Midfielder: 'Mediocampista',
      Forward: 'Delantero',
    }[position] ?? position
  )
}

function rarityLabel(scarcity: number): string {
  if (scarcity <= 35) return 'leyenda'
  if (scarcity <= 70) return 'difícil'
  return 'común'
}

function initials(name: string): string {
  return name
    .split(' ')
    .slice(0, 2)
    .map((part) => part[0])
    .join('')
    .toUpperCase()
}

function countryIndex(): number {
  return countries.findIndex((country) => country.code === selectedCountryCode)
}

function countryByOffset(offset: number): Country | null {
  if (countries.length === 0) {
    return null
  }
  const nextIndex = (countryIndex() + offset + countries.length) % countries.length
  return countries[nextIndex] ?? null
}

function stripeStyle(colors: string[]): string {
  const usableColors = colors.length > 0 ? colors : ['#75aadb', '#ffffff', '#75aadb']
  return `style="--stripe-colors: ${usableColors.join(', ')};"`
}

async function loadCountries(): Promise<void> {
  countries = await apiGet<Country[]>(`/api/countries?collector_slug=${collectorSlug}`)
}

async function loadCountry(code: string): Promise<void> {
  selectedCountryCode = code
  pageTurning = true
  render()
  selectedPage = await apiGet<CountryPage>(`/api/countries/${code}/stickers?collector_slug=${collectorSlug}`)
  window.setTimeout(() => {
    pageTurning = false
    render()
  }, 240)
}

async function openPack(): Promise<void> {
  notice = ''
  lastPack = await apiPost<PackResult>(`/api/collectors/${collectorSlug}/packs/open`)
  await loadCountries()
  await loadCountry(selectedCountryCode)
}

function countryButtons(): string {
  return countries
    .map(
      (country) => `
        <button class="country-tab ${country.code === selectedCountryCode ? 'is-active' : ''}" data-country="${country.code}">
          <span>${countryName(country.name)}</span>
          <small>${country.code}</small>
          <strong>${country.owned_stickers}/${country.total_stickers}</strong>
        </button>
      `,
    )
    .join('')
}

function stickerCard(sticker: Sticker): string {
  const rarity = rarityLabel(sticker.scarcity)
  const slot = selectedPage ? selectedPage.stickers.findIndex((item) => item.id === sticker.id) + 1 : 0
  const revealedPhoto =
    sticker.owned && sticker.image_url
      ? `<img src="${sticker.image_url}" alt="${sticker.name}" loading="lazy" />`
      : `<span>${sticker.owned ? initials(sticker.name) : '?'}</span>`
  return `
    <article class="sticker ${sticker.owned ? 'is-owned' : 'is-missing'}">
      <div class="sticker-shine"></div>
      <div class="sticker-topline">
        <span>${selectedPage?.code ?? 'WC'}</span>
        <b>${rarity}</b>
      </div>
      <div class="sticker-photo ${rarity}">
        ${revealedPhoto}
      </div>
      <div class="sticker-meta">
        <strong>${sticker.owned ? sticker.name : `Figu ${slot.toString().padStart(2, '0')}`}</strong>
        <span>${sticker.owned ? positionName(sticker.position) : 'Sin pegar'}</span>
      </div>
      <div class="sticker-status">${sticker.owned ? 'pegada' : 'falta'}</div>
    </article>
  `
}

function packStrip(): string {
  if (!lastPack) {
    return ''
  }
  if (!lastPack.opened) {
    return `<div class="pack-strip"><strong>${notice}</strong><span>0 sobres disponibles</span></div>`
  }
  return `
    <div class="pack-strip">
      <strong class="pack-title">Último sobre</strong>
      ${lastPack.stickers
        .map(
          (sticker) => `
            <span class="pack-pull ${sticker.is_new ? 'is-new' : ''}">
              ${sticker.is_new ? 'Nueva' : 'Repetida'} · ${sticker.country_code} · ${sticker.name}
            </span>
          `,
        )
        .join('')}
    </div>
  `
}

function albumPage(): string {
  if (!selectedPage) {
    return '<section class="album-spread"></section>'
  }
  const country = countries.find((item) => item.code === selectedPage?.code)
  const previousCountry = countryByOffset(-1)
  const nextCountry = countryByOffset(1)
  return `
    <section class="album-spread ${pageTurning ? 'is-turning' : ''}" ${stripeStyle(selectedPage.stripe_colors)}>
      <div class="album-cover-strip">
        <span>Copa Mundial 2026</span>
        <strong>Álbum de figus</strong>
      </div>
      <div class="album-page">
        <div class="page-header">
          <div>
            <span class="eyebrow">Selección ${selectedPage.code}</span>
            <h1>${countryName(selectedPage.name)}</h1>
            <p>Plantel actual para completar, pegar y sufrir con dignidad.</p>
          </div>
          <div class="progress-stamp">
            <strong>${country?.owned_stickers ?? 0}</strong>
            <span>de ${country?.total_stickers ?? selectedPage.stickers.length}</span>
          </div>
        </div>
        <div class="sticker-grid">
          ${selectedPage.stickers.map(stickerCard).join('')}
        </div>
        <div class="page-nav">
          <button class="page-button" type="button" data-country="${previousCountry?.code ?? selectedCountryCode}">
            <span>Anterior</span>
            <strong>${previousCountry ? countryName(previousCountry.name) : ''}</strong>
          </button>
          <button class="page-button" type="button" data-country="${nextCountry?.code ?? selectedCountryCode}">
            <span>Siguiente</span>
            <strong>${nextCountry ? countryName(nextCountry.name) : ''}</strong>
          </button>
        </div>
      </div>
    </section>
  `
}

function render(): void {
  if (loading) {
    app.innerHTML = '<main class="shell"><section class="album-spread loading-page"></section></main>'
    return
  }

  app.innerHTML = `
    <main class="shell ${sidebarOpen ? '' : 'is-sidebar-collapsed'}">
      <aside class="sidebar">
        <div class="brand">
          <span>Figus</span>
          <strong>2026</strong>
        </div>
        <div class="sidebar-copy">
          <strong>Mi álbum</strong>
          <span>Pasá de selección y abrí dos sobres diarios.</span>
        </div>
        <nav class="country-list" aria-label="Selecciones">
          ${countryButtons()}
        </nav>
        <button class="pack-button" id="open-pack" type="button">
          <span>Abrir sobre</span>
          <strong>5</strong>
        </button>
      </aside>
      <button class="sidebar-toggle" id="sidebar-toggle" type="button">
        ${sidebarOpen ? 'Ocultar selecciones' : 'Ver selecciones'}
      </button>
      <div class="album">
        ${albumPage()}
        ${packStrip()}
      </div>
    </main>
  `

  document.querySelectorAll<HTMLButtonElement>('[data-country]').forEach((button) => {
    button.addEventListener('click', () => {
      const code = button.dataset.country
      if (code && code !== selectedCountryCode) {
        void loadCountry(code)
      }
    })
  })
  document.querySelector<HTMLButtonElement>('#open-pack')?.addEventListener('click', () => {
    void openPack()
  })
  document.querySelector<HTMLButtonElement>('#sidebar-toggle')?.addEventListener('click', () => {
    sidebarOpen = !sidebarOpen
    render()
  })
}

async function boot(): Promise<void> {
  try {
    await loadCountries()
    await loadCountry(selectedCountryCode)
  } catch {
    notice = 'API no disponible'
  } finally {
    loading = false
    render()
  }
}

void boot()
