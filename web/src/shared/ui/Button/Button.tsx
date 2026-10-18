import { cn } from "cn"
import type { ComponentProps } from "react"

import { buttonVariants, type ButtonVariantProps } from "./buttonVariants"

export type ButtonProps = ComponentProps<"button"> &
  ButtonVariantProps & {
    /** Показывает спиннер, блокирует кнопку и выставляет aria-busy. */
    loading?: boolean
    /** Растягивает кнопку на всю ширину контейнера. */
    fullWidth?: boolean
  }

function ButtonSpinner() {
  return (
    <span
      aria-hidden="true"
      className="size-4 shrink-0 animate-spin rounded-full border-2 border-current border-t-transparent"
    />
  )
}

/**
 * Базовая кнопка (shared/ui).
 *
 * @example
 * <Button>Сохранить</Button>
 * <Button variant="outline" size="sm">Отмена</Button>
 * <Button variant="destructive" loading={isPending}>Удалить</Button>
 * <Button size="icon" aria-label="Закрыть"><X /></Button>
 */
export function Button({
  className,
  variant = "default",
  size = "default",
  loading = false,
  fullWidth = false,
  disabled,
  type = "button",
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      data-slot="button"
      data-loading={loading || undefined}
      type={type}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      className={cn(
        buttonVariants({ variant, size }),
        fullWidth && "w-full",
        className
      )}
      {...props}
    >
      {loading && <ButtonSpinner />}
      {children}
    </button>
  )
}
